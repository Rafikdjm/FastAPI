"""
Test de bcrypt pour vérifier qu'il fonctionne
Exécutez : python test_bcrypt.py
"""

def test_bcrypt():
    print("🔍 Test de bcrypt")
    print("=" * 60)
    
    try:
        from passlib.context import CryptContext
        
        # Créer le contexte
        bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        print("✅ CryptContext créé avec succès")
        
        # Tester le hash
        password = "RafikDM@06"
        hashed = bcrypt_context.hash(password)
        print(f"✅ Hash créé : {hashed[:20]}...")
        
        # Tester la vérification
        is_valid = bcrypt_context.verify(password, hashed)
        if is_valid:
            print("✅ Vérification réussie")
        else:
            print("❌ Vérification échouée")
        
        # Tester avec un mauvais mot de passe
        is_valid = bcrypt_context.verify("mauvais_mdp", hashed)
        if not is_valid:
            print("✅ Rejet du mauvais mot de passe")
        else:
            print("❌ Le mauvais mot de passe a été accepté !")
        
        print("\n" + "=" * 60)
        print("🎉 Bcrypt fonctionne correctement!")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        print("👉 Installez : pip install bcrypt")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print(f"   Type : {type(e).__name__}")
        print("\n💡 Solutions :")
        print("   1. pip install bcrypt")
        print("   2. pip install --upgrade passlib[bcrypt]")
        print("   3. pip install py-bcrypt")
        return False

if __name__ == "__main__":
    test_bcrypt()