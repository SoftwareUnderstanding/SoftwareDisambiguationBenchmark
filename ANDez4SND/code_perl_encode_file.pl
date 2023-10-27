#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open ':std', ':encoding(UTF-8)';
use Encode;

# Check for proper command line arguments
if (@ARGV != 2) {
    die "Usage: $0 input_file output_file\n";
}

# File names from command line arguments
my ($input_file, $output_file) = @ARGV;

# Open input file for reading with UTF-8 encoding
open my $in_fh, '<:encoding(UTF-8)', $input_file or die "Cannot open $input_file: $!\n";

# Open output file for writing with UTF-8 encoding
open my $out_fh, '>:encoding(UTF-8)', $output_file or die "Cannot open $output_file: $!\n";

# Process each line from the input file
while (my $line = <$in_fh>) {
    # Do some processing on $line if needed

    # Write the processed line to the output file
    print $out_fh $line;
}

# Close the filehandles
close $in_fh;
close $out_fh;

print "Done! Data has been processed and written to the output file.\n";
