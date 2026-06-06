from main import cadastrar_tutor, login_tutor, cadastrar_pet
print("--- SIMULADOR DO FRONT END // CADASTRO ---")
while True:
    print("\nO que você gostaria de testar?")
    print("[1] Cadastro do Tutor (Create)")
    print("[2] Login do Tutor")
    print("[3] Cadastro do Pet")
    print("[4] Visualizar Ficha do Tutor (Read)")
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

    elif escolha == "0":
        print("Saindo do simulador...")
        break

    else:
        print("Opção inválida")


