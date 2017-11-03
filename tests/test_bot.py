# Integration test
import pytest
import sys
sys.path.append('/Users/alice/Desktop/BotForSecurity')
from BotForSecurity.Bot import *

def test_handle():
	
	# Test invalid input
	actual_return_1 = handle_message("Hello",None, None, "Counts").lower()
	expected_return_1 = "counts"
	# Test valid subcommand yet not following its master command
	actual_return_2 = handle_message("Specific 1",None, None, "Counts").lower()
	expected_return_2 = "counts"
	# Test valid subcommand
	actual_return_3 = handle_message("Specific 1",None, None, "Specific").lower()
	expected_return_3 = "specific"
	assert(actual_return_1 == expected_return_1)
	assert(actual_return_2 == expected_return_2)
	assert(actual_return_3 == expected_return_3)
