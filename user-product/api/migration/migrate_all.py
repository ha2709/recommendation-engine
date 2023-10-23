import subprocess

# Run the migrations
subprocess.run(["python3", "migration/user.py"])
subprocess.run(["python3", "migration/product.py"])
subprocess.run(["python3", "migration/transaction.py"])
