import argparse
import json
import requests

def main(context_data, output_file):
  try:
    with open(context_data) as f:
      context_data = json.load(f)

    # prepare context
    context = str(context_data[0]["details"])
  except Exception:
    import traceback
    context = str(traceback.format_exc())

  # prepare response
  output_response = [{
      "index": 0,
      "success": True,
      "input_type": "text",
      "is_url": False,
      "details": {},
      "input_segment_info": [],
      "attributes": { "data": context },
  }]
  # save response in output_file
  with open(output_file, "w") as f:
    json.dump(output_response, f)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--context_data", type=str, required=True)
  parser.add_argument("--output_file", type=str, required=True)
  args = parser.parse_args()

  context_data = args.context_data
  output_file = args.output_file
  main(context_data, output_file)