import datetime
import hashlib


class Block:
  num_block = None
  data = None
  createdAt = datetime.datetime.now()
  nonce = 0

  def __init__(self,
               data: dict,
               num_block: int,
               previous_hash: str,
               process_id: int):
    self.data = data
    self.num_block = num_block
    self.process_id = process_id
    self.previous_hash = previous_hash

  def hash(self):
    h = hashlib.sha256()

    h.update(
      str(self.process_id).encode('utf-8') +
      str(self.previous_hash).encode('utf-8') +
      str(self.nonce).encode('utf-8') +
      str(self.num_block).encode('utf-8') +
      str(self.data).encode('utf-8')
    )

    return h.hexdigest()
