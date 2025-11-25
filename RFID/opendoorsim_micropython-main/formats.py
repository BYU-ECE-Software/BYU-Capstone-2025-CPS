# Wiegand_Formats.py - Dictionary of Wiegand formats

# --- Wiegand Format Definitions ---
# This dictionary holds all desired Wiegand card formats.
# Most formats are taken from https://www.everythingid.com.au/hid-card-formats-i-15
# Key is the number of bits received for the format.
# Each value is a dictionary containing:
#   'name': A human-readable name for the format.
#   'facility_code': A dict with 'start' and 'end' bit positions (inclusive) for the facility code.
#   'card_number': A dict with 'start' and 'end' bit positions (inclusive) for the card number.
#   'parity_checks': A list of dictionaries, one for each parity bit. Each dict contains:
#       'parity_bit_pos': The actual bit position where the parity bit is located.
#       'data_bits': A LIST of bit positions that are included in the calculation for this parity bit.
#                    This handles both contiguous ranges (using list(range(start, end+1)))
#                    and staggered/non-contiguous bit positions.
#       'type': 'even' or 'odd' parity.


WIEGAND_FORMATS = {
    26: {
        "name": "STANDARD 26-bit (H10301)",
        "facility_code": {"start": 1, "end": 8},
        "card_number": {"start": 9, "end": 24},
        "parity_checks": [
            {"parity_bit_pos": 0, "data_bits": list(range(1, 13)), "type": "even"}, # Even parity over bits 1-12
            {"parity_bit_pos": 25, "data_bits": list(range(13, 25)), "type": "odd"}, # Odd parity over bits 13-24
        ]
    },
    32: {
        "name": "ATS WIEGAND 32-Bit",
        "facility_code": {"start": 1, "end": 13},
        "card_number": {"start": 14, "end": 30},
        "parity_checks": [
            {"parity_bit_pos": 0, "data_bits": list(range(1, 14)), "type": "even"}, 
            {"parity_bit_pos": 31, "data_bits": list(range(14, 31)), "type": "odd"},
        ]
    },
    34: {
        "name": "HID STANDARD 34-Bit",
        "facility_code": {"start": 1, "end": 16},
        "card_number": {"start": 17, "end": 32}, 
        "parity_checks": [
            {"parity_bit_pos": 0, "data_bits": list(range(1, 17)), "type": "even"}, 
            {"parity_bit_pos": 33, "data_bits": list(range(17, 33)), "type": "odd"},
        ]
    },
    35: {
        "name": "HID 35BIT CORPORATE 1000",
        "facility_code": {"start": 2, "end": 13},
        "card_number": {"start": 14, "end": 33}, 
        "parity_checks": [
            {"parity_bit_pos": 1, "data_bits": [2,3,5,6,8,9,11,12,14,15,17,18,20,21,23,24,26,27,29,30,32,33], "type": "even"}, 
            {"parity_bit_pos": 34, "data_bits": [1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23,25,26,28,29,31,32], "type": "odd"},
        ]
    },
    37: {
        "name": "HID 37-bit (H10302)",
        "facility_code": {},
        "card_number": {"start": 1, "end": 35},
        "parity_checks": [
            {"parity_bit_pos": 0, "data_bits": list(range(1, 19)), "type": "even"}, # Even parity over first 18 data bits
            {"parity_bit_pos": 36, "data_bits": list(range(19, 36)), "type": "odd"}, # Odd parity over last 18 data bits
        ]
    },
    48: {
        "name": "HID 48BIT CORPORATE 1000 (H2004064)",
        "facility_code": {"start": 2, "end": 23},
        "card_number": {"start": 24, "end": 46}, 
        "parity_checks": [
            {"parity_bit_pos": 1, "data_bits": [3,4,6,7,9,10,12,13,15,16,18,19,21,22,24,25,27,28,30,31,33,34,36,37,39,40,42,43,45,46], "type": "even"}, 
            {"parity_bit_pos": 47, "data_bits": [2,3,5,6,8,9,11,12,14,15,17,18,20,21,23,24,26,27,29,30,32,33,35,36,38,39,41,42,44,45], "type": "odd"},
        ]
    }
}
