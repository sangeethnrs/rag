:: Create main directories
mkdir data\raw
mkdir data\processed
mkdir data\vector_store
mkdir src\processing
mkdir src\vectorstore
mkdir src\rag
mkdir src\config
mkdir src\utils
mkdir ui\pages
mkdir ui\components
mkdir tests
mkdir logs
mkdir scripts

:: Create data subdirectories
mkdir data\raw\auto\icici
mkdir data\raw\auto\tata
mkdir data\raw\health\icici
mkdir data\raw\health\tata

:: Create Python files - using echo. > to create empty files
echo. > .env
echo. > requirements.txt
echo. > README.md
echo. > .gitignore

:: Create Python package files
echo. > src\__init__.py
echo. > src\processing\__init__.py
echo. > src\processing\document_processor.py
echo. > src\processing\text_splitter.py
echo. > src\vectorstore\__init__.py
echo. > src\vectorstore\vector_store.py
echo. > src\rag\__init__.py
echo. > src\rag\retriever.py
echo. > src\rag\chain.py
echo. > src\config\__init__.py
echo. > src\config\settings.py
echo. > src\utils\__init__.py
echo. > src\utils\helpers.py

:: Create UI files
echo. > ui\__init__.py
echo. > ui\pages\chat.py
echo. > ui\pages\document_upload.py
echo. > ui\components\chat_interface.py

:: Create test files
echo. > tests\__init__.py
echo. > tests\test_document_processor.py
echo. > tests\test_vector_store.py
echo. > tests\test_rag.py

:: Create script files
echo. > scripts\setup.py
echo. > scripts\process_documents.py