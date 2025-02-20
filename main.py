import streamlit as st
from scrape import scrape_website
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content
)
from parse import parse_with_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping website")

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("Dom Content",cleaned_content,height=300)


if "dom_content" in st.session_state:
    # taking user prompt
    parse_description = st.text_area("Describe what you want to parse ?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the Content")

            # chunks/batches
            dom_batches = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_batches,parse_description)
            st.write(result)

    