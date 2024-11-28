.EXPORT_ALL_VARIABLES:

# Install dependencies
install:
	cd debiaiServer && pip install -r requirements.txt
	cd frontend && npm install

# Run the application in development mode
run_debiaiServer:
	python run_debiai_server_dev.py

run_frontend:
	cd frontend && npm run serve

start:
	make run_debiaiServer & make run_frontend

code:
	code debiaiServer
	code frontend


# Code quality
format:
	# -----  Formatting Python code with Black
	cd debiaiServer && black .

	# -----  Formatting JavaScript code with Prettier
	cd frontend && npm run prettier

check:
	# -----  Validating Black code style
	cd debiaiServer && black --check --diff .

	# -----  Validating Flake8 code style
	cd debiaiServer && flake8 .

	# -----  Validating Prettier code style
	cd frontend && npm run prettier:check

	# -----  Validating CSpell errors
	cspell .

	# ----- The code is formatted correctly
