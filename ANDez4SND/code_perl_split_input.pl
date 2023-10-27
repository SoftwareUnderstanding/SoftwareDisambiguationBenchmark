#!/usr/bin/perl
use strict;
use warnings;

# Check for proper command line arguments
if (@ARGV != 3) {
    die "Usage: $0 input_file output_file_70_percent output_file_30_percent\n";
}

# File names from command line arguments
my ($input_file, $output_file_70, $output_file_30) = @ARGV;

# Open input file for reading
open my $in_fh, '<', $input_file or die "Cannot open $input_file: $!\n";

# Read all lines from input file into an array
my @lines = <$in_fh>;

# Close input file
close $in_fh;

# Calculate 70% of the number of lines
my $seventy_percent_count = int(@lines * 0.7 + 0.5);

# Randomly shuffle the array of lines
use List::Util 'shuffle';
@lines = shuffle @lines;

# Split the array into 70% and 30%
my @seventy_percent = @lines[0 .. $seventy_percent_count - 1];
my @thirty_percent = @lines[$seventy_percent_count .. $#lines];

# Write 70% subset to output file
open my $out_70_fh, '>', $output_file_70 or die "Cannot open $output_file_70: $!\n";
print $out_70_fh @seventy_percent;
close $out_70_fh;

# Write 30% subset to output file
open my $out_30_fh, '>', $output_file_30 or die "Cannot open $output_file_30: $!\n";
print $out_30_fh @thirty_percent;
close $out_30_fh;

print "Done! Data has been split into 70% and 30% subsets.\n";
