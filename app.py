import streamlit as st
import random
import string
import pyperclip # Used for clipboard integration

# --- 1. Character Sets ---
LOWER_CHARS = string.ascii_lowercase
UPPER_CHARS = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = string.punctuation

# --- 2. Generation Logic ---
def generate_strong_password(length, use_lower, use_upper, use_digits, use_symbols):
    """Generates a random password based on user selections and ensures security rules."""
    
    all_chars = []
    
    # Add selected character sets
    if use_lower:
        all_chars.extend(LOWER_CHARS)
    if use_upper:
        all_chars.extend(UPPER_CHARS)
    if use_digits:
        all_chars.extend(DIGITS)
    if use_symbols:
        all_chars.extend(SYMBOLS)

    if not all_chars:
        return None, "Error: You must select at least one character type."

    # --- Security Rule: Ensure at least one of each selected type is present ---
    # This is a good practice for strong passwords
    password_list = []
    
    if use_lower:
        password_list.append(random.choice(LOWER_CHARS))
    if use_upper:
        password_list.append(random.choice(UPPER_CHARS))
    if use_digits:
        password_list.append(random.choice(DIGITS))
    if use_symbols:
        password_list.append(random.choice(SYMBOLS))

    # Fill the rest of the password length randomly
    remaining_length = length - len(password_list)
    if remaining_length < 0:
        remaining_length = 0
        
    filler_chars = [random.choice(all_chars) for _ in range(remaining_length)]
    password_list.extend(filler_chars)

    # Shuffle the list to ensure the required characters aren't always at the start
    random.shuffle(password_list)
    
    return "".join(password_list), None

# --- 3. Streamlit UI (GUI Design) ---
st.set_page_config(page_title="Strong Password Generator", layout="centered")

st.title("🔐 Advanced Password Generator")
st.markdown("Create highly secure, customizable passwords instantly.")
st.markdown("---")

# --- User Customization & Input Validation ---
with st.container(border=True):
    st.subheader("Settings")
    
    # Password Length
    length = st.slider("Password Length (Minimum 8)", 
                       min_value=8, max_value=32, value=12, step=1)
    
    # Character Set Preferences
    st.markdown("**Character Types:**")
    col1, col2 = st.columns(2)
    with col1:
        use_lower = st.checkbox("Lowercase (a-z)", value=True)
        use_upper = st.checkbox("Uppercase (A-Z)", value=True)
    with col2:
        use_digits = st.checkbox("Numbers (0-9)", value=True)
        use_symbols = st.checkbox("Symbols (!@#$)", value=True)

# Generate Button
if st.button("✨ Generate Password", type="primary"):
    # Security Rule: Length check
    if length < 8:
        st.error("Length must be at least 8 for a secure password.")
    # Security Rule: Character type check
    elif not any([use_lower, use_upper, use_digits, use_symbols]):
        st.error("You must select at least one character type.")
    else:
        password, error_msg = generate_strong_password(
            length, use_lower, use_upper, use_digits, use_symbols
        )
        
        if password:
            # Store the generated password in session state
            st.session_state['generated_password'] = password
            st.success("Password Generated Successfully!")

# --- Output and Clipboard Integration ---
if 'generated_password' in st.session_state and st.session_state['generated_password']:
    st.markdown("---")
    st.subheader("Your Generated Password:")
    
    col_output, col_copy = st.columns([4, 1])
    
    with col_output:
        st.code(st.session_state['generated_password'], language="text")
    
    # Clipboard Integration
    with col_copy:
        if st.button("📋 Copy"):
            try:
                pyperclip.copy(st.session_state['generated_password'])
                st.toast("Copied to clipboard!")
            except pyperclip.PyperclipException:
                st.warning("Could not automatically copy. Please copy the text manually.")