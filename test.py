import requests
import re

def find_php_modules_and_extensions(repo_owner, repo_name, file_path, predefined_extensions):
    # Provide your GitHub personal access token
    access_token = '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'

    # Construct the GitHub API URL
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'

    # Set up the request headers with the access token
    headers = {
        'Authorization': f'Token {access_token}',
        'Accept': 'application/vnd.github.v3.raw',
    }

    try:
        # Make a request to get the content of the PHP file
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        file_content = response.text

        modules_and_extensions = {
            'include': set(),
            'require': set(),
            'namespace': set(),
            'extension': set()
        }

        # Find include statements
        include_matches = re.findall(r'\binclude\s*\(?.*?[\'"](.*?)[\'"]\)?\s*;?', file_content)
        modules_and_extensions['include'].update(include_matches)

        # Find require statements
        require_matches = re.findall(r'\brequire\s*\(.*?[\'"](.*?)[\'"]\s*\)?\s*;?\s*', file_content)
        modules_and_extensions['require'].update(require_matches)

        # Find namespace declarations
        namespace_matches = re.findall(r'\bnamespace\s+(.*?)[;{]', file_content)
        modules_and_extensions['namespace'].update(namespace_matches)

        # Find predefined extensions
        for extension in predefined_extensions:
            extension_matches = re.findall(r'\b' + extension + r'\b', file_content)
            modules_and_extensions['extension'].update(extension_matches)

        return modules_and_extensions

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    repo_owner = 'PuneethReddyHC'  # Replace with the repository owner
    repo_name = 'online-shopping-system-advanced'  # Replace with the repository name
    file_path = 'admin/server/server.php'  # Replace with the file path within the repository

    predefined_extensions = ['mysqli_connect', 'mysqli_close', 'mysqli_select_db', 'mysqli_query', 'mysqli_fetch_assoc', 'mysqli_fetch_row', 'mysqli_fetch_array', 'mysqli_num_rows', 'mysqli_affected_rows', 'mysqli_insert_id', 'mysqli_error', 'mysqli_prepare', 'mysqli_stmt_bind_param', 'mysqli_stmt_execute', 'mysqli_stmt_get_result', 'mysqli_free_result', 'mysqli_begin_transaction', 'mysqli_commit', 'mysqli_rollback', 'mysqli_real_escape_string','curl_init', 'curl_setopt', 'curl_exec', 'curl_getinfo', 'curl_error', 'curl_close', 'curl_version','imagecreate', 'imagecreatetruecolor', 'imagecopyresampled', 'imagecolorallocate', 'imagecopymerge', 'imagedestroy', 'imagepng', 'imagejpeg', 'imagegif', 'imagesx', 'imagesy','mb_strlen', 'mb_substr', 'mb_strtolower', 'mb_strtoupper', 'mb_convert_case', 'mb_convert_encoding', 'mb_detect_encoding', 'mb_internal_encoding', 'mb_convert_variables', 'mb_encode_numericentity', 'mb_decode_numericentity', 'mb_convert_kana', 'mb_substr_count', 'mb_strpos', 'mb_stripos', 'mb_strrpos', 'mb_strripos', 'mb_strstr', 'mb_strrchr', 'mb_strwidth', 'mb_strimwidth', 'mb_check_encoding', 'mb_http_input', 'mb_http_output', 'mb_language', 'mb_list_encodings', 'mb_encoding_aliases', 'mb_convert_variables', 'mb_encode_mimeheader', 'mb_decode_mimeheader', 'mb_send_mail','hash', 'hmac', 'md5', 'sha1', 'sha256', 'sha512', 'password_hash', 'crypt', 'session', 'session_start', 'session_name', 'session_id', 'session_regenerate_id', 'session_destroy', 'session_unset','json', 'json_decode', 'json_encode', 'json_last_error', 'json_last_error_msg','openssl', 'openssl_cipher_iv_length', 'openssl_csr_export', 'openssl_csr_export_to_file', 'openssl_csr_new', 'openssl_csr_sign','openssl_error_string', 'openssl_free_key', 'openssl_get_cert_locations', 'openssl_get_cipher_methods', 'openssl_get_md_methods','openssl_get_privatekey', 'openssl_get_publickey', 'openssl_open', 'openssl_pbkdf2', 'openssl_pkcs12_export', 'openssl_pkcs12_export_to_file','openssl_pkcs12_read', 'openssl_pkcs7_decrypt', 'openssl_pkcs7_encrypt', 'openssl_pkcs7_sign', 'openssl_pkcs7_verify', 'openssl_pkey_export','openssl_pkey_export_to_file', 'openssl_pkey_free', 'openssl_pkey_get_details', 'openssl_pkey_get_private', 'openssl_pkey_get_public','openssl_pkey_new', 'openssl_private_decrypt', 'openssl_private_encrypt', 'openssl_public_decrypt', 'openssl_public_encrypt', 'openssl_random_pseudo_bytes','openssl_seal', 'openssl_sign', 'openssl_spki_export', 'openssl_spki_export_challenge', 'openssl_spki_new', 'openssl_spki_verify','openssl_verify', 'openssl_x509_check_private_key', 'openssl_x509_checkpurpose', 'openssl_x509_export', 'openssl_x509_export_to_file','openssl_x509_fingerprint', 'openssl_x509_free', 'openssl_x509_parse', 'openssl_x509_read','pdo', 'PDO', 'PDOException', 'PDOStatement', 'PDOException','xml', 'xml_error_string', 'xml_get_current_byte_index', 'xml_get_current_column_number', 'xml_get_current_line_number', 'xml_get_error_code', 'xml_parse', 'xml_parse_into_struct', 'xml_get_character_data_handler', 'xml_set_character_data_handler', 'xml_set_default_handler', 'xml_set_element_handler', 'xml_set_end_namespace_decl_handler', 'xml_set_external_entity_ref_handler', 'xml_set_notation_decl_handler', 'xml_set_processing_instruction_handler', 'xml_set_start_namespace_decl_handler', 'xml_set_unparsed_entity_decl_handler', 'xml_error', 'xml_get_current_byte_index', 'xml_parser_create', 'xml_parser_create_ns', 'xml_parser_free', 'xml_parser_get_option', 'xml_parser_set_option', 'xml_parse_into_struct', 'xml_parse', 'xml_set_character_data_handler', 'xml_set_default_handler', 'xml_set_element_handler', 'xml_set_end_namespace_decl_handler', 'xml_set_external_entity_ref_handler', 'xml_set_notation_decl_handler', 'xml_set_processing_instruction_handler', 'xml_set_start_namespace_decl_handler', 'xml_set_unparsed_entity_decl_handler', 'xml_set_object', 'xml_set_element_handler', 'xml_set_character_data_handler', 'xml_set_processing_instruction_handler', 'xml_set_default_handler', 'xml_set_unparsed_entity_decl_handler', 'xml_set_notation_decl_handler', 'xml_set_external_entity_ref_handler', 'xml_set_start_namespace_decl_handler', 'xml_set_end_namespace_decl_handler', 'xml_set_object', 'xml_set_element_handler', 'xml_set_character_data_handler', 'xml_set_processing_instruction_handler', 'xml_set_default_handler', 'xml_set_unparsed_entity_decl_handler', 'xml_set_notation_decl_handler', 'xml_set_external_entity_ref_handler', 'xml_set_start_namespace_decl_handler', 'xml_set_end_namespace_decl_handler', 'xml_set_object','zip_open', 'zip_read', 'zip_close', 'zip_entry_open', 'zip_entry_close', 'zip_entry_read', 'zip_entry_filesize', 'zip_entry_name', 'zip_entry_compressedsize', 'zip_entry_compressionmethod', 'zip_entry_time', 'zip_entry_crc', 'zip_entry_write', 'zip_entry_rename', 'zip_entry_set', 'zip_entry_filemtime', 'zip_entry_set', 'zip_entry_set' ]  # Add more extensions as needed
    result = find_php_modules_and_extensions(repo_owner, repo_name, file_path, predefined_extensions)

    if result:
        print("Included modules:")
        print(result['include'])

        print("\nRequired modules:")
        print(result['require'])

        print("\nNamespaces:")
        print(result['namespace'])

        print("\nUsed extensions:")
        print(result['extension'])
