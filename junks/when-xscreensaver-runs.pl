#!/usr/bin/perl
# execute when idle

my $blanked = 0;
open (IN, "xscreensaver-command -watch |");
while (<IN>) {
    if (m/^(BLANK|LOCK)/) {
        if (!$blanked) {        # if previous state is not blank
            exec('bash ~/.whenidle');
            $blanked = 1;
        }
    } elsif (m/^UNBLANK/) {
        $blanked = 0;
    }
}
