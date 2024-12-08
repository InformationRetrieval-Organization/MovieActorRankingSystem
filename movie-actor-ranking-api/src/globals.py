def init_globals():
    """
    Initialize the global variables
    """
    global _vocabulary
    global _document_frequency
    global _document_term_weight_matrix
    global _document_id_vector_map
    global _U_reduced
    global _S_reduced
    global _V_reduced
    global _document_svd_matrix
    global _classifier
    global _classified_actors_vector_map

    _vocabulary = []  # List of str
    _document_frequency = {}
    _document_term_weight_matrix = []
    _document_id_vector_map = {}
    _U_reduced = []
    _S_reduced = []
    _V_reduced = []
    _document_svd_matrix = {}
    _classifier = None
    _classified_actors_vector_map = {}
