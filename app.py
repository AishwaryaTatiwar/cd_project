import streamlit as st

# Define the grammar rules
grammar = {
    'S': [['NP', 'VP']],
    'NP': [['Det', 'N'], ['PN']],
    'VP': [['V', 'NP'], ['V', 'PP']],
    'PP': [['P', 'NP']],
    'Det': ['the', 'a', 'an'],
    'N': ['man', 'dog', 'cat', 'ball', 'house'],
    'PN': ['John', 'Mary'],
    'V': ['hit', 'saw', 'kicked', 'ran', 'ate'],
    'P': ['with', 'in', 'on', 'at']
}

# Define first sets
first_sets = {
    'S': ['the', 'a', 'an', 'John', 'Mary'],
    'NP': ['the', 'a', 'an', 'John', 'Mary'],
    'VP': ['hit', 'saw', 'kicked', 'ran', 'ate'],
    'PP': ['with', 'in', 'on', 'at'],
    'Det': ['the', 'a', 'an'],
    'N': ['man', 'dog', 'cat', 'ball', 'house'],
    'PN': ['John', 'Mary'],
    'V': ['hit', 'saw', 'kicked', 'ran', 'ate'],
    'P': ['with', 'in', 'on', 'at']
}

# Define follow sets
follow_sets = {
    'S': ['$'],
    'NP': ['hit', 'saw', 'kicked', 'ran', 'ate', 'with', 'in', 'on', 'at', '$'],
    'VP': ['$'],
    'PP': ['hit', 'saw', 'kicked', 'ran', 'ate', 'with', 'in', 'on', 'at', '$'],
    'Det': ['man', 'dog', 'cat', 'ball', 'house'],
    'N': ['hit', 'saw', 'kicked', 'ran', 'ate', 'with', 'in', 'on', 'at', '$'],
    'PN': ['hit', 'saw', 'kicked', 'ran', 'ate', 'with', 'in', 'on', 'at', '$'],
    'V': ['the', 'a', 'an', 'John', 'Mary', 'with', 'in', 'on', 'at'],
    'P': ['the', 'a', 'an', 'John', 'Mary']
}

# LL(1) Parsing Table
parsing_table = {
    'S': {
        'the': ['NP', 'VP'],
        'a': ['NP', 'VP'],
        'an': ['NP', 'VP'],
        'John': ['NP', 'VP'],
        'Mary': ['NP', 'VP']
    },
    'NP': {
        'the': ['Det', 'N'],
        'a': ['Det', 'N'],
        'an': ['Det', 'N'],
        'John': ['PN'],
        'Mary': ['PN']
    },
    'VP': {
        'hit': ['V', 'NP'],
        'saw': ['V', 'NP'],
        'kicked': ['V', 'NP'],
        'ran': ['V', 'PP'],
        'ate': ['V', 'PP']
    },
    'PP': {
        'with': ['P', 'NP'],
        'in': ['P', 'NP'],
        'on': ['P', 'NP'],
        'at': ['P', 'NP']
    },
    'Det': {
        'the': ['the'],
        'a': ['a'],
        'an': ['an']
    },
    'N': {
        'man': ['man'],
        'dog': ['dog'],
        'cat': ['cat'],
        'ball': ['ball'],
        'house': ['house']
    },
    'PN': {
        'John': ['John'],
        'Mary': ['Mary']
    },
    'V': {
        'hit': ['hit'],
        'saw': ['saw'],
        'kicked': ['kicked'],
        'ran': ['ran'],
        'ate': ['ate']
    },
    'P': {
        'with': ['with'],
        'in': ['in'],
        'on': ['on'],
        'at': ['at']
    }
}

class LL1Parser:
    def __init__(self, grammar, parsing_table):
        self.grammar = grammar
        self.parsing_table = parsing_table
        self.stack = ['$', 'S']  # Initialize stack with $ and start symbol
        
    def parse(self, tokens):
        tokens.append('$')  # Add end marker
        token_index = 0
        derivation = []
        
        while len(self.stack) > 0:
            top = self.stack[-1]
            current_token = tokens[token_index]
            
            if top == current_token:
                # Match
                self.stack.pop()
                token_index += 1
            elif top in self.grammar:
                # Non-terminal - expand using parsing table
                try:
                    production = self.parsing_table[top][current_token]
                    self.stack.pop()
                    # Push production in reverse order
                    for symbol in reversed(production):
                        if symbol != 'ε':  # Skip epsilon productions
                            self.stack.append(symbol)
                    derivation.append(f"{top} -> {' '.join(production)}")
                except KeyError:
                    return False, derivation  # No production in parsing table
            else:
                return False, derivation  # Mismatch
            
        return token_index == len(tokens), derivation

def tokenize(sentence):
    return sentence.split()

st.title("English Grammar Checker with LL(1) Parser")
st.write("This app checks if a sentence is grammatically correct using an LL(1) parser.")

input_sentence = st.text_input("Enter an English sentence:", value="the man hit the ball")

if st.button("Check Grammar"):
    if not input_sentence.strip():
        st.warning("Please enter a sentence.")
    else:
        tokens = tokenize(input_sentence)
        parser = LL1Parser(grammar, parsing_table)
        is_valid, derivation = parser.parse(tokens.copy())
        
        st.subheader("Result:")
        if is_valid:
            st.success("✅ The sentence is grammatically correct!")
        else:
            st.error("❌ The sentence is not grammatically correct.")
        
        st.subheader("Parsing Details:")
        st.write(f"Input sentence: {input_sentence}")
        st.write(f"Tokens: {tokens}")
        
        if derivation:
            st.write("Derivation steps:")
            for step in derivation:
                st.write(step)
        else:
            st.write("No valid derivation found.")

st.markdown("""
### Notes:
- This is a simplified grammar checker that only handles basic English sentences.
- The grammar covers simple noun phrases, verb phrases, and prepositional phrases.
- Example valid sentences:
  - "the man hit the ball"
  - "John saw a cat"
  - "Mary ate in the house"
""")