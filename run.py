from app import create_app

import os
#os.environ["OMP_NUM_THREADS"] = "2"
#os.environ["TF_NUM_INTRAOP_THREADS"] = "2"
#os.environ["TF_NUM_INTEROP_THREADS"] = "2"

app = create_app()

# Expose app and db to Flask CLI
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
