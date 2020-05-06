# SAG-Projekt
Projekt z przedmiotu Systemy Agentowe


## Instalacja systemu
Aby uruchomić system należy zainstalować serwer XMPP oraz całe środowisko Pythona.
Jako serwer XMPP wybrany został serwer `prosody`. W celu jego instalacji należy wpisać w terminal `apt-get install prosody`. Do kontroli i konfiguracji serwera wykorzystujemy narzędzie `prosodyctl`. Aby zrestartować serwer należy wykonać polecenie `prosodyctl restart`. Aby dodać nowego użytkownika (agenta) należy wykonać polecenie `prosodyctl adduser nazwa@localhost`. Po uruchomieniu tego polecenia, zostaniesz poproszony/a o hasło dla danego użytkownika/agenta. (Ważne, serwer nie jest skonfigurowany pod żadną konkretną domenę, dlatego trzeba użyć `localhost` a nie żadne `127.0.0.1` czy coś innego). 

Drugim krokiem jest instalacja środowiska Pythona. W tym celu należy wykorzystać narzędzie `pipenv`. Po sklonowaniu repozytorium, wykonujemy polecenie `pipenv install`. Utworzy ono wirtualne środowisko oraz zainstaluje wszystkie potrzebne pakiety, w tym `spade`. Aby uruchomić wirtualne środowisko, wpisujemy polecenie `pipenv shell`. W wirtualnym środowisku mamy dostęp do wersji Pythona opisanej w pliku `Pipfile`, wraz z wszystkimi potrzebnymi pakietami. Do instalacji nowych pakietów nie wykorzystujemy `pip install <pakiet>` tylko `pipenv install <pakiet>`, dzięki temu mamy pewność że informacja o nowym pakiecie pojawi się w pliku `Pipfile` i inni będą mogli to szybko zainstalować.

