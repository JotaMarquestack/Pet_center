from main import cadastrar_tutor, login_tutor, cadastrar_pet, visualizar_tutor, atualizar_pet, redefinir_senha_tutor, atualizar_perfil_tutor, deletar_tutor_completo, remover_pet

print("--- SIMULADOR DO FRONT END // CADASTRO ---")
while True:
    print("\nO que você gostaria de testar?")
    print("[1] Cadastro do Tutor (Create)")
    print("[2] Login do Tutor")
    print("[3] Cadastro do Pet")
    print("[4] Visualizar Ficha do Tutor (Read)")
    print("[5] Atualizar Dados do Pet (Update)")
    print("[6] Atualizar Perfil do Tutor (Nome/Telefone)")
    print("[7] Redefinir Senha do Tutor")
    print("[8] Remover um Pet do Sistema (Delete)")         
    print("[9] Excluir Cadastro do Tutor Inteiro (Delete)")
    print("[0] Sair")
    escolha = input ("Escolha uma opção: ")

    if escolha == "1":
        print("\n--- TELA DE CADASTRO ---")
        nome_tutor = input("Digite seu Nome Completo: ")
        c = input("Digite seu CPF: ")
        t = input("Digite seu Telefone: ")
        e = input("Digite seu E-mail: ")
        s = input("Digite sua Senha: ")

        resposta = cadastrar_tutor(c, nome_tutor, t, e, s)
        print(resposta)

    elif escolha == "2":
        print("\n--- TELA DE LOGIN ---")
        e = input("Digite seu E-mail: ")
        s = input("Digite sua Senha: ")
        
        resposta = login_tutor(e, s)
        print(resposta)

    elif escolha == "3":
        print("\n--- TELA DE CADASTRO DO PET ---")
        e_tutor = input("E-mail do tutor: ")
        nome_pet = input("Nome do Pet: ")
        esp = input("Espécie do Pet: ")
        raca_pet = input("Raça do Pet: ")
        peso_pet = input("Peso do Pet (em Kg): ")
        sexo_pet = input("Sexo (M/F): ").upper()
        obs_pet = input("Observações Médicas: ")

        castrado_input = input("O pet é castrado? (S/N): ")
        is_castrado = castrado_input.upper() == "S"
        while castrado_input not in ["S", "N"]:
            print("Por favor, digite apenas 'S' ou 'N'.")
            castrado_input = input("O pet é castrado? (S/N): ")

        resposta = cadastrar_pet(e_tutor, nome_pet, esp, raca_pet, peso_pet, is_castrado, sexo_pet, obs_pet)
        print(resposta)
    
    elif escolha == "4":
        print("\n--- CONSULTA DA FICHA ---")
        e = input("Digite o e-mail do tutor que deseja consultar: ")
        
        resposta = visualizar_tutor(e)
        print(resposta)
    
    elif escolha == "5":
        print("\n--- ATUALIZAÇÃO DE PRONTUÁRIO ---")
        id_p = input("Digite o ID do pet (ex: PET-XXXXXX): ").upper().strip()
        n_peso = input("Digite o novo peso do Pet (em Kg): ")

        castrado_input = input("O pet agora é castrado? (S/N): ").upper()
        while castrado_input not in ["S", "N"]:
            print("Por favor, digite apenas S para Sim ou N para Não.")
            castrado_input = input("O pet agora é castrado? (S/N): ").upper()
        n_castrado = castrado_input == "S"

        n_obs = input("Novas observações médicas: ")

        resposta = atualizar_pet(id_p, n_peso, n_castrado, n_obs)
        print(resposta)
    
    elif escolha == "6":
        print("\n--- ATUALIZAR PERFIL DO TUTOR ---")
        e = input("Digite o E-mail do tutor que deseja alterar: ")
        n_nome = input("Digite o NOVO Nome: ")
        n_tel = input("Digite o NOVO Telefone: ")

        resposta = atualizar_perfil_tutor(e, n_tel, n_nome)
        print(resposta)
    
    elif escolha == "7":
        print("\n--- REDEFINIR SENHA ---")
        e = input("Digite o E-mail do tutor: ")
        n_senha = input("Digite a NOVA Senha: ")

        resposta = redefinir_senha_tutor(e, n_senha)
        print(resposta)
    
    elif escolha == "8":
        print("\n--- REMOÇÃO DE PET ---")
        id_p = input("Digite o ID do pet que deseja remover: ").upper().strip()

        certeza = input(f"Tem certeza que deseja apagar o pet {id_p}? (S/N): ").upper()
        if certeza == "S":
            resposta = remover_pet(id_p)
            print(resposta)
        else:
            print("Operação cancelada.")
    
    elif escolha == "9":
        print("\n--- EXCLUSÃO TOTAL DE CADASTRO ---")
        e = input("Digite o E-mail do tutor que será APAGADO do sistema: ")

        print("ALERTA: Isso apagará o tutor e todos os animais vinculados a ele!")
        certeza = input(f"Tem certeza absoluta que deseja continuar? (S/N): ").upper()
        if certeza == "S":
            resposta = deletar_tutor_completo(e)
            print(resposta)
        else:
            print("Operação cancelada.")

    elif escolha == "0":
        print("Saindo do simulador...")
        break

    else:
        print("Opção inválida")


