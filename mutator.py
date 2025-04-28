
# from dos_finder import * # This is to import the mutator stuff
from generic_mutator_bytes import * # This is needed for mutate_generic...
from xml_mutators.main import fuzz as fuzz_xml # This is the actual fuzz function for the bullshit stuff...
import io
import zipfile

import string

ascii_chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace

def mutate_random_byte(data: bytes) -> bytes:
	if not data:
		return data  # Return unchanged if empty
	index = random.randint(0, len(data) - 1)
	new_byte = ord(random.choice(ascii_chars))
	return data[:index] + bytes([new_byte]) + data[index + 1:]

def mutate_xml_contents(fn: str, original_contents: bytes):
	assert isinstance(original_contents, bytes) # Should be of type bytes
	new = mutate_random_byte(original_contents)
	return new # Just a dummy for now.




def main_mutation_function(fn: str, original_contents: bytes):
	# Does the thing...

	# Choose mutation strategy first...
	mut_funcs = [mutate_xml_contents, fuzz_xml] # This has the handler shit. the mutate_xml_contents is from this file, but the "fuzz" is from xml_mutators/main.py

	mut_strat = random.choice(mut_funcs)

	# Now run the shit...
	if mut_strat == fuzz_xml:
		res = fuzz_xml(original_contents) # Just pass in the original bytes...
	else:
		res = mut_strat(fn, original_contents) # Pass it to the thing 


	return res




def mutate_xml(zip_bytes, modify_func): # Thanks to ChatGPT!!!
	# Read original ZIP from memory
	input_zip = io.BytesIO(zip_bytes)
	with zipfile.ZipFile(input_zip, 'r') as zip_in:
		# Store the modified contents
		modified_files = {}
		# Here instead of mutating each file, just choose one and mutate it instead.
		shit = zip_in.namelist()
		target_file_name = random.choice(zip_in.namelist())
		for file_name in zip_in.namelist():
			if file_name == target_file_name:
				with zip_in.open(file_name) as f:
					original_content = f.read()
					modified_content = modify_func(file_name, original_content)
					modified_files[file_name] = modified_content
			else:
				# Now just do the stuff...
				with zip_in.open(file_name) as f:
					original_content = f.read()
					# modified_content = modify_func(file_name, original_content)
					modified_files[file_name] = original_content # Just copy the original contents...
	# Create a new ZIP file in memory
	output_zip = io.BytesIO()
	with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zip_out:
		for file_name, content in modified_files.items():
			zip_out.writestr(file_name, content)

	return output_zip.getvalue()


def init(seed):
	pass

def deinit():
	pass

def fuzz(buf, add_buf, max_size): # For AFL and AFL++

	data = buf

	#print(str(type(data)) * 100)

	#assert (isinstance(data, bytes))

	data = bytes(data) # Convert bytearray to bytes.
	try:
		data = mutate_xml(data, main_mutation_function)
	except:
		return buf

	if len(data) >= max_size:
		print("Truncating returned fuzz data...\n")
		print("Orig len is " + str(len(data)) + " . New len is " + str(max_size))
		data = data[:max_size] # Truncate

	data = bytearray(data) # Convert bytes back to bytearray.

	return data

TEST_MUT_COUNT=1000
TEST_FILENAME = "samplefile.xlsx"
TEST_OUTPUT = "output.xlsx"

def load_test_data():
	fh = open(TEST_FILENAME, "rb")
	data = fh.read()
	fh.close()
	return data

def save_test_data(data):
	fh = open(TEST_OUTPUT, "wb")
	fh.write(data)
	fh.close()
	return

def test_mut():
	# Tests the mutator.
	test_data = load_test_data()
	for _ in range(TEST_MUT_COUNT):
		# Run the thing...
		test_data = mutate_xml(test_data, main_mutation_function)
	save_test_data(test_data)
	return

if __name__=="__main__":
	test_mut()
	exit()

