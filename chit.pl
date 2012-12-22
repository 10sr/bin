#!/usr/bin/env perl

# very simple note taking app
# basically no way to remove note
# each note can be only one line.

# usage :

# chit [-ac] [-l] <note>

use strict;
use warnings;

use File::Spec;
use File::Path 'mkpath';

print "I am Chit!", "\n";

sub print_help {
    warn "chit: usage: chit [-ac] [-l] <note>", "\n";
}

################################
# subs for add chit

sub get_time {
    my ($sec, $min, $hour, $mday, $mon, $year) = localtime();
    $year += 1900;
    $mon += 1;
    my $str1 = sprintf('%04d%02d', $year, $mon);
    my $str2 = sprintf('%02d%02d%02d%02d', $mday, $hour, $min, $sec);
    return $str1, $str2;
}

sub write_file {
    my ($path, $file, $str) = @_;
    mkpath($path);
    my $filepath = File::Spec->catfile($path, $file);

    open my $fh, ">", $filepath or
        die qq/Can't open file "$file": $!/;
    print $fh $str, "\n";
    close $fh or die qq/Can't close file "$file": $!/;

    print "Add chit: '$filepath'", "\n";
    print "    $str", "\n";
    return
}

sub add_chit {
    my $chitpath = shift @_;
    my $str = join(" ", @_);
    my ($dir, $file) = get_time();
    my $path = File::Spec->catfile($chitpath, $dir);
    write_file($path, $file, $str)
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

sub format_path_to_time {
    # .config/chit/201212/22182340 => 2012/12/22 18:23:40
    my $path = shift;
    if ($path =~ m#(\d{4})(\d{2})/(\d{2})(\d{2})(\d{2})(\d{2})#) {
        return "$1/$2/$3 $4:$5:$6";
    } else {
        return
    }
}

sub cat_one_file {
    my $file = shift;
    open my $fh, '<', $file
        or die qq/Can't open file "$file": $!/;
    my $line = <$fh>;            # only read one line
    close $fh;
    return $line;
}

sub cat_files {
    # return number of files processed
    my ($path, $num) = @_;
    my @files = sort { $b cmp $a } grep { /\d{8}$/ } get_files($path);
    my $i = 0;
    foreach my $file (@files) {
        eval {
            my $timestr = format_path_to_time($file);
            my $line = cat_one_file($file);
            print "$timestr $line";
            $i += 1;
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
    my $chitpath = shift @_;
    my @dirs = sort { $b cmp $a } grep { /\d{6}$/ } get_files($chitpath);
    my $num = 10;               # number of chit to cat
    foreach my $d (@dirs) {
        my $i = cat_files($d, $num);
        $num -= $i;

        if ($num <= 0) {
            return;
        }
    }
}

my $homepath = $ENV{'HOME'};
if (! $homepath) {
    warn "HOME is not set. Use current directory.", "\n";
    $homepath = "."
}
my $confpath = $ENV{'XDG_CONFIG_HOME'} ||
    File::Spec->catfile($homepath, ".config");
my $chitpath = File::Spec->catfile($confpath, "chit");

if (@ARGV == 0) {
    print_help();
} elsif (index($ARGV[0], "a") == 0) {
    shift @ARGV;
    add_chit($chitpath, @ARGV);
} elsif (index($ARGV[0], "c") == 0) {
    shift @ARGV;
    cat_chit($chitpath, @ARGV);
} else {
    print_help();
}
