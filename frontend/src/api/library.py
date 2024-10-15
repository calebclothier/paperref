import pandas as pd
import streamlit as st


def load_library_for_user():
    # mock data
    test_data = [
        [
            '10.1103/PhysRevX.12.021028',
            'Universal gate operations on nuclear spin qubits in an optical tweezer array of 171Yb atoms', 
        ],
        [
            '10.1038/s41467-022-32094-6', 
            'Erasure conversion for fault-tolerant quantum computing in alkaline earth Rydberg atom arrays', 
        ],
        [
            '10.1038/s41586-023-06438-1', 
            'High-fidelity gates with mid-circuit erasure conversion in a metastable neutral atom qubit', 
        ]
    ]
    df = pd.DataFrame(test_data, columns=['DOI', 'Title'])
    return df

def save_library_for_user():
    print(st.session_state.id_token)
    print(st.session_state.refresh_token)