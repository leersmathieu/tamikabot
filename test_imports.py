#!/usr/bin/env python3
"""Script de vérification rapide des imports et de la structure du bot."""

import sys

def test_imports():
    """Vérifie que tous les modules s'importent correctement."""
    print("🔍 Vérification des imports...")
    
    try:
        from bot import Bot, Config
        print("✅ Bot et Config importés")
    except Exception as e:
        print(f"❌ Erreur import Bot/Config: {e}")
        return False
    
    try:
        from bot.cogs import Art, Bank, Google, Joke, Lfg, Messages, Reminder, Stream
        print("✅ Tous les Cogs importés")
    except Exception as e:
        print(f"❌ Erreur import Cogs: {e}")
        return False
    
    try:
        from bot.db.database import BankDatabase, ReminderDatabase
        print("✅ Databases importées")
    except Exception as e:
        print(f"❌ Erreur import Databases: {e}")
        return False
    
    return True

def test_cog_commands():
    """Vérifie que les commandes ont des docstrings."""
    print("\n🔍 Vérification des docstrings des commandes...")
    
    from bot.cogs import Art, Bank, Google, Joke, Messages, Reminder, Stream
    
    cogs_to_check = [
        (Art, ['ascii']),
        (Bank, ['add_coins', 'bank']),
        (Google, ['google_search', 'translate']),
        (Joke, ['say_joke', 'say_joke_tts']),
        (Messages, ['delete_messages', 'say']),
        (Reminder, ['remind', 'list_reminders', 'cancel_reminder']),
        (Stream, ['play', 'skip', 'queue', 'leave', 'pause', 'resume', 'stop', 'reset']),
    ]
    
    all_good = True
    for cog_class, methods in cogs_to_check:
        cog_name = cog_class.__name__
        for method_name in methods:
            method = getattr(cog_class, method_name, None)
            if method is None:
                print(f"❌ {cog_name}.{method_name} n'existe pas")
                all_good = False
                continue
            
            docstring = method.__doc__
            if not docstring or not docstring.strip():
                print(f"❌ {cog_name}.{method_name} n'a pas de docstring")
                all_good = False
            elif "Arguments:" not in docstring and method_name in ['ascii', 'add_coins', 'google_search', 'translate', 'delete_messages', 'say', 'remind', 'cancel_reminder', 'play']:
                print(f"⚠️  {cog_name}.{method_name} manque la section Arguments")
                all_good = False
            else:
                print(f"✅ {cog_name}.{method_name} - docstring OK")
    
    return all_good

if __name__ == "__main__":
    print("=" * 60)
    print("Test de vérification TamikaBot")
    print("=" * 60)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_cog_commands():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Tous les tests sont passés !")
        sys.exit(0)
    else:
        print("❌ Certains tests ont échoué")
        sys.exit(1)
