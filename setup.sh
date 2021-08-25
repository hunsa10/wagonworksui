mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"dfroes@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "[theme]
primaryColor='#094ee4'
backgroundColor='#f1f1f0'
secondaryBackgroundColor='#c2d2e9'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
