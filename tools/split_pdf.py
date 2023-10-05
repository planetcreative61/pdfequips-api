import subprocess
import tempfile
import os

import subprocess
import tempfile
import os

def split_by_range(input_file, ranges):
    try:
        # Save the input file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_input:
            temp_input.write(input_file.read())
            temp_input_path = temp_input.name

        # Generate the output file names based on the range
        output_files = []
        for i, range_obj in enumerate(ranges):
            output_file = f"output-{i}.pdf"
            output_files.append(output_file)

            # Run the pdfseparate command for each range
            subprocess.run(['pdfseparate', '-f', str(range_obj['from']), '-l',
                           str(range_obj['to']), temp_input_path, output_file], check=True)

        print("PDF split successfully.")
        return output_files
    except subprocess.CalledProcessError as e:
        print(f"Error splitting PDF: {e}")
        return []
    finally:
        # Remove the temporary input file
        if temp_input_path:
            os.remove(temp_input_path)
