#!/usr/bin/env perl

# very simple note taking app
# basically no way to remove note

use strict;
use warnings;

use File::Spec;
use File::Path 'mkpath';
use File::Path 'rmtree';
use Term::ANSIColor;

sub print_help {
    warn
        "chit: usage: chit {a|add} <note>\n" .
        "        or:  chit {c|cat}[<num>] [<pattern>]\n" .
        "        or:  chit {l|load} <files>\n" .
        "        or:  chit {d|dump}[<num>] [<pattern>]\n"
        ;
}

##################################
# format time and path

sub get_time {
    # return time string in format like 2012/12/22 18:23:40
    my ($sec, $min, $hour, $mday, $mon, $year) = localtime();
    $year += 1900;
    $mon += 1;
    return sprintf('%04d/%02d/%02d %02d:%02d:%02d',
                   $year, $mon, $mday, $hour, $min, $sec);
}

sub format_path_to_time {
    # .config/chit/201212/22182340 => 2012/12/22 18:23:40
    my $path = shift;
    # \D is separator
    if ($path =~ m#(\d{4})(\d{2})\D*?(\d{2})(\d{2})(\d{2})(\d{2})$#) {
        return "$1/$2/$3 $4:$5:$6";
    } else {
        return;
    }
}

sub format_time_to_path {
    # 2012/12/22 18:23:40 => 201212, 22182340
    my $time = shift;
    if ($time =~ m#(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2})$#) {
        my $dir = "$1$2";
        my $file = "$3$4$5$6";
        return ($dir, $file);
    } else {
        return;
    }
}

################################
# subs for add chit

sub write_file {
    my ($path, $file, $str) = @_;
    mkpath($path);
    my $filepath = File::Spec->catfile($path, $file);

    open my $fh, ">", $filepath or
        die qq/Can't open file "$file": $!/;
    print $fh "${str}\n";
    close $fh or die qq/Can't close file "$file": $!/;

    return;
}

sub add_chit {
    my $chitpath = shift @_;
    my $str;
    if (@_ == 0) {
        print ">> ";
        $str = <STDIN>;
    } else {
        $str = join(" ", @_);
    }
    my $time = get_time();
    my ($dir, $file) = format_time_to_path($time);
    my $path = File::Spec->catfile($chitpath, $dir);
    if ($str) {
        write_file($path, $file, $str);
        $str = colored($str, 'bold');
        print
            "Add chit: '$dir/$file'\n" .
            "    $str\n";
    } else {
        print "Empty chit.\n";
    }
    return;
}

#################################
# subs for cat chits

sub get_files {
    # get files undir $1 with path
    my $dir = shift;

    opendir my $dh, $dir
      or die qq/Can't open directory "$dir": $!/;

    my @dirs = map { "$dir/$_" } grep { $_ ne '.' && $_ ne '..' } readdir $dh;

    return @dirs;
}

sub cat_one_file {
    # open file and return content
    my ($file, $pattern) = @_;
    open my $fh, '<', $file
        or die qq/Can't open file "$file": $!/;
    my $line = <$fh>;            # only read one line
    close $fh;
    if (! $pattern || $line =~ /$pattern/) {
        return $line;
    } else {
        return;
    }
}

sub cat_files {
    # cat files under given directory
    # return number of files used
    my ($path, $num, $pattern, $nocolor, $fh) = @_;
    my @files = sort { $b cmp $a } grep { /\d{8}$/ } get_files($path);
    my $i = 0;
    foreach my $file (@files) {
        eval {
            my $timestr = format_path_to_time($file);
            my $line = cat_one_file($file, $pattern);
            if ($line) {
                if (! $nocolor) { $line = colored($line, 'bold'); }
                if ($fh) {
                    print $fh "$timestr $line";
                } else {
                    print "$timestr $line";
                }
                $i += 1;
            }
        };
        if ($@) {
            warn qq/Error while cat file: $@/;
        }

        if ($i >= $num && $num != 0) { # if $num is 0 cat all files
            return $i;
        }
    }

    return $i;
}

sub cat_chit {
    my ($chitpath, $num, $pattern, $nocolor, $fh) = @_;
    my @dirs = sort { $b cmp $a } grep { /\d{6}$/ } get_files($chitpath);
    if ($num < 0) {
        $num = 10;
    }
    foreach my $d (@dirs) {
        my $i = cat_files($d, $num, $pattern, $nocolor, $fh);
        $num -= $i;

        if ($num <= 0) {
            return;
        }
    }
    return;
}

##############################
# subs for dump

sub dump_chit {
    my ($path, $num, $pattern) = @_;
    cat_chit($path, $num, $pattern, 1);
    return;
}

##############################
# subs for archiving

sub archive_dir {
    my ($dir, $backuppath) = @_;
    if ($dir =~ /\D(\d*)$/) {
        my $basename = $1;
        my $file = File::Spec->catfile($backuppath, $basename . ".txt");
        # what if file already exists?
        open my $fh, ">", $file or
            die qq/Can't open file "$file": $!/;
        cat_files($dir, 0, undef, 1, $fh);
        # remove dir
        rmtree($dir);
    }
    return;
}

sub archive_old_dirs {
    my ($chitpath, $backuppath) = @_;
    mkpath($backuppath);
    my @dirs = sort { $b cmp $a} grep { /\d{6}$/ } get_files($chitpath);
    my $num = 0;                # number of dirs
    foreach my $d (@dirs) {
        $num += 1;
        if ($num > 12) {
            archive_dir($d, $backuppath);
        }
    }
    return;
}

################################
# subs for load chits

sub load_line {
    my ($chitpath, $line) = @_;
    if ($line =~ m#^(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) (.*)$#) {
        my $time = $1;
        my $content = $2;
        my ($dir, $file) = format_time_to_path($time);
        my $path = File::Spec->catfile($chitpath, $dir);
        write_file($path, $file, $content);
    }
    return;
}

sub load_file {
    my ($chitpath, $file) = @_;
    if ($file) {
        open my $fh, "<", $file or
            die qq/Can't open file "$file" : $!/;
        while (my $line = <$fh>) {
            load_line($chitpath, $line);
        }
    } else {
        while (my $line = <STDIN>) {
            load_line($chitpath, $line);
        }
    }
    return;
}

sub load_chit {
    my $chitpath = shift;
    my @files = @_;
    if (@files != 0) {
        foreach my $file (@files) {
            load_file($chitpath, $file);
        }
    } else {
        load_file($chitpath);
    }
    return;
}

#################################
# setup directory

sub get_chitpath {
    my $homepath = $ENV{'HOME'};
    if (! $homepath) {
        warn "HOME is not set. Use current directory.\n";
        $homepath = "."
    }
    my $confpath = $ENV{'XDG_CONFIG_HOME'} ||
        File::Spec->catfile($homepath, ".config");
    my $chitpath = File::Spec->catfile($confpath, "chit");
    my $backuppath = File::Spec->catfile($chitpath, "backup");

    my $env_chitpath = $ENV{"CHIT_PATH"};
    if ($env_chitpath) { $chitpath = $env_chitpath; }
    return ($chitpath, $backuppath);
}

sub extract_num {
    # extract number from string, return -1 if none
    my $str = shift;
    if ($str =~ /^\D*(\d+)/) {   # number of chit to cat
        return $1;
    } else {
        return -1;
    }
}

if (@ARGV == 0) {
    print_help();
} else {
    my ($chitpath, $backuppath) = get_chitpath();
    my $cmd = shift;
    my $beg = substr $cmd, 0, 1;
    if ($beg eq "a") {
        add_chit($chitpath, @ARGV);
    } elsif ($beg eq "c") {
        my $num = extract_num($cmd);
        cat_chit($chitpath, $num, $ARGV[0]);
    } elsif ($beg eq "d") {
        my $num = extract_num($cmd);
        dump_chit($chitpath, $num, $ARGV[0]);
    } elsif ($beg eq "l") {
        load_chit($chitpath, @ARGV);
    } else {
        print_help();
    }
    archive_old_dirs($chitpath, $backuppath);
}
