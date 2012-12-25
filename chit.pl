#!/usr/bin/env perl

# very simple note taking app
# basically no way to remove note
# each note can be only one line.

use strict;
use warnings;

use File::Spec;
use File::Path 'mkpath';
use Term::ANSIColor;

sub print_help {
    warn
        "chit: usage: chit a[ad] <note>\n" .
        "        or:  chit c[at][<num>] [<pattern>]\n"
        ;
}

##################################
# format time and path

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
    # 2012/12/22 18:23:40 => 201212/22182340
    my $time = shift;
    if ($time =~ m#(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2})$#) {
        my $dir = "$1$2";
        my $file = "$3$4$5$6";
        return File::Spec->catfile($dir, $file);
    } else {
        return;
    }
}

################################
# subs for add chit

sub get_time {
    # return time string in format like 2012/12/22 18:23:40
    my ($sec, $min, $hour, $mday, $mon, $year) = localtime();
    $year += 1900;
    $mon += 1;
    return sprintf('%04d/%02d/%02d %02d:%02d:%02d',
                   $year, $mon, $mday, $hour, $min, $sec);
}

sub write_file {
    my ($path, $file, $str) = @_;
    mkpath($path);
    my $filepath = File::Spec->catfile($path, $file);

    open my $fh, ">", $filepath or
        die qq/Can't open file "$file": $!/;
    print $fh "${str}\n";
    close $fh or die qq/Can't close file "$file": $!/;

    return
}

sub add_chit {
    my $chitpath = shift @_;
    my $str = join(" ", @_);
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
}

#################################
# subs for cat chits

sub get_files {
    my $dir = shift;

    opendir my $dh, $dir
      or die qq/Can't open directory "$dir": $!/;

    my @dirs = map { "$dir/$_" } grep { $_ ne '.' && $_ ne '..' } readdir $dh;

    return @dirs;
}

sub cat_one_file {
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
    my ($path, $num, $pattern) = @_;
    my @files = sort { $b cmp $a } grep { /\d{8}$/ } get_files($path);
    my $i = 0;
    foreach my $file (@files) {
        eval {
            my $timestr = format_path_to_time($file);
            my $line = cat_one_file($file, $pattern);
            if ($line) {
                $line = colored($line, 'bold');
                print "$timestr $line";
                $i += 1;
            }
        };
        if ($@) {
            warn qq/Error while cat file: $@/;
        }

        if ($i == $num) {
            return $i;
        }
    }

    return $i;
}

sub cat_chit {
    my ($chitpath, $num, $pattern) = @_;
    my @dirs = sort { $b cmp $a } grep { /\d{6}$/ } get_files($chitpath);
    if ($num =~ /\D*(\d+)/) {   # number of chit to cat
        $num = $1;
    } else {
        $num = 10;
    }
    foreach my $d (@dirs) {
        my $i = cat_files($d, $num, $pattern);
        $num -= $i;

        if ($num <= 0) {
            return;
        }
    }
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
    return $chitpath;
}

if (@ARGV == 0) {
    print_help();
} else {
    my $chitpath = get_chitpath();
    my $cmd = shift;
    my $beg = substr $cmd, 0, 1;
    if ($beg eq "a") {
        add_chit($chitpath, @ARGV);
    } elsif ($beg eq "c") {
        my $num = substr $cmd, 1;
        cat_chit($chitpath, $num, @ARGV);
    } elsif ($beg eq "d") {
        dump_chit($chitpath, @ARGV);
    } elsif ($beg eq "l") {
        load_chit($chitpath, @ARGV);
    } else {
        print_help();
    }
}
