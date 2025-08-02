import hashlib

def hash_function(data):
  # Using sha256 for demonstration, but a faster non-crypto hash like xxHash is better.
  return hashlib.sha256(data).hexdigest()

def generate_k_hash(data_stream, chunk_size):
  # 1. Chunk the data
  chunks = [data_stream[i:i+chunk_size] for i in range(0, len(data_stream), chunk_size)]
  n = len(chunks)

  # 2. Process through lenses
  positional_hashes = []
  frequency_map = {}
  relational_hashes = []

  # Process positional and frequency in one loop
  for i, chunk in enumerate(chunks):
    # Lens 1: Positional
    positional_input = chunk + str(i).encode()
    positional_hashes.append(hash_function(positional_input))

    # Lens 2: Frequency
    content_hash = hash_function(chunk)
    frequency_map[content_hash] = frequency_map.get(content_hash, 0) + 1

  # Process relational in a separate loop
  for i in range(n - 1):
    # Lens 3: Relational
    relational_input = chunks[i] + chunks[i+1]
    relational_hashes.append(hash_function(relational_input))

  # 3. Assemble the final K-Hash object
  k_hash_object = {
    "chunk_size": chunk_size,
    "total_chunks": n,
    "positional_hashes": positional_hashes,
    "frequency_hashes": frequency_map,
    "relational_hashes": relational_hashes
  }

  return k_hash_object

# --- Example Usage ---
# file_data = open("my_document.txt", "rb").read()
# k_hash = generate_k_hash(file_data, 1024)
# print(k_hash)
