# graf wejściowy, użyłem listy zamiast z pliku zczytywać, ale zamysł jest ten sam.
# Każda linijka ma wzór [wierzchołek od]-[wierzchołek do]:[długość]
graph = [
    "3-2:54.4",
    "12-3:4.5",
    "2-5:34.65",
    "5-3:2.4",
    "3-12:1.00",
]
# wierzchołki
vertices = []
# długości
distances = {}
# ten kod leci linijkę po linijce i dodaje wierzchołki i długości do naszych pustych zmiennych
for line in graph:
    start_vertex = int(line[:line.find('-')])
    end_vertex = int(line[line.find('-')+1:line.find(":")])
    vertices.append(start_vertex)
    vertices.append(end_vertex)
    weight = float(line[line.find(":")+1:])
    # dodajemy dystans od startu do sąsiada (używam słownika pythonowego, czyli zbiór par klucz: wartość)
    # na przykład, dla wierzchołka 3 będzie to wyglądać następująco:
    # {
    #    3: {2: 54.4, 12: 1.00}
    # }
    # czyli klucz to wierzchołek (3), a wartość to wszystkie krawędzie które od niego wychodzą
    # a to też jest w formie słownika, gdzie klucz to końcowy wierzchołek (2, 12), a wartość do długość (czy tam waga)
    try:
        distances[start_vertex][end_vertex] = weight
    except KeyError:
        distances[start_vertex] = {end_vertex: weight}

# przekształcam listę w zbiór pythonowy - to jest tylko po to żeby się pozbyć duplikatów
# czyli vertices to docelowo lista wszystkich wierzchołków w grafie
vertices = set(vertices)
print('vertices: ', vertices)
print('distances: ', distances)


def dijkstra(vertices, distances, start):
    """
    Algorytm Dijkstry.
    Wejście:
    vertices - lista wierzchołków
    distances - lista dystansów (wag), według wzoru wierzchołek: {sąsiad1: dystans1, sąsiad2: dystans2, ...}
    start - nazwa wierzchołka startowego
    """
    # wierzchołki, które jeszcze nie oblecieliśmy, plus ich wartości
    # uwaga: użyłem tutaj wartości null jako nieskończoność
    # uwaga 2: mówiąc 'nieoblecone', mam na myśli wierzchołki, które jeszcze nie były
    # obecnym wierzchołkiem w algorytmie (czyli te, których wszystkich sąsiadów jeszcze nie sprawdziliśmy)
    # mam nadzieję, że zrobi to większy sens w dalszych komentarzach
    unvisited = {vertex: None for vertex in vertices}
    # sprawdzamy czy wierzchołek startowy w ogóle istnieje
    if start not in vertices:
        print("Nie ma wierzchołka {} w grafie".format(start))
        return
    # obleciane wierzchołki
    visited = {}
    # punkty, z których chcemy dotrzeć do danego wierzchołka (czyli tak jakby rodzice każdego wierzchołka)
    # to będzie przydatne żeby wypisywać punkty, jakie odwiedzić, by się dokądś dostać
    travel_paths = {}
    # ustawiamy obecny punkt jako start
    current_vertex = start
    # zmienna która przechowuje dystans jaki do tej pory przebyliśmy (na razie 0, rzecz jasna)
    curr_distance = 0
    # ustawiamy wartość do startowego wierzchołka jako 0 (wiadomo, już tu jesteśmy)
    unvisited[current_vertex] = curr_distance

    # lecimy dopóki są jeszcze jakieś nieobleciane wierzchołki
    while unvisited:
        print('current vertex: {}'.format(current_vertex))
        print('current distance: {}'.format(curr_distance))
        # sprawdzamy sąsiadów naszego wierzchołka (current_vertex),
        # bierzemy sąsiadów oraz dystanse z zmiennej distances
        for neighbour, distance in distances[current_vertex].items():
            print('checking {} with a distance of {}'.format(neighbour, distance))
            # jak sąsiad już został obleciany, pomijamy go
            # continue tu oznacza przejdź do następnego sąsiada
            if neighbour not in unvisited:
                continue
            # idziemy do sąsiada, dodajemy dystans do niego do naszego obecnego dystansu
            new_distance = curr_distance + distance
            # teraz sprawdzamy wartość sąsiada z listy wierzchołków, które jeszcze nie oblecieliśmy
            # przypadek 1: jeszcze ani razu nie byliśmy u sąsiada, czyli jego wartość to nieskończoność
            if unvisited[neighbour] is None:
                print('{} is unvisited, so take distance {}'.format(neighbour, new_distance))
                # czyli ustawiamy, że na razie najkrótszy dystans do sąsiada to obecny (ten z current_vertex do sąsiada)
                unvisited[neighbour] = new_distance
                # tutaj kluczowy punkt: ustawiamy nasz obecny wierzchołek jako punkt,
                # przez który trzeba przejść, żeby dostać się do sąsiada
                print('Also, set {} as travel path for {}'.format(current_vertex, neighbour))
                travel_paths[neighbour] = current_vertex
            # przypadek 2: już znaleźliśmy jakąś drogę do sąsiada, ale mamy teraz lepszą (i.e. mniejszy dystans)
            elif unvisited[neighbour] > new_distance:
                print('{} is visited (distance: {}), but shorter dist found, so take distance {}'.format(neighbour, unvisited[neighbour], new_distance))
                # czyli nadpisujemy poprzedni dystans tym nowym, lepszym
                unvisited[neighbour] = new_distance
                # i kolejny kluczowy punkt: nadpisujemy punkt, przez który trzeba przejść, żeby dostać się do sąsiada
                # w ten sposób wiemy, jak dostać się do każdego punktu w grafie
                print('Also, set {} as new travel path for {}'.format(current_vertex, neighbour))
                travel_paths[neighbour] = current_vertex
        # przejrzeliśmy wszystkich sąsiadów naszego obecnego wierzchołka, więc możemy go 'odhaczyć'
        visited[current_vertex] = curr_distance
        # usuwamy wierzchołek z listy nieobleconych punktów
        del unvisited[current_vertex]
        # poniżej decydujemy, który wierzchołek sprawdzić jako następny
        # patrzymy na dystanse, jakie już mamy zapisane dla jeszcze nieoblecianych punktów
        # i wybieramy wierzchołek z najmniejszą wartością
        if unvisited:
            candidates = [city for city in unvisited.items() if city[1]]
            best_candidate, curr_distance = sorted(candidates, key=lambda x:x[1])[0]
            # ustawiamy wierzchołek z najniższą wartością jako nasz nowy obecny, i lecimy od początku
            current_vertex = best_candidate

    # zwracamy listę oblecianych wierzchołków (każdy będzie miał swoją wagę trasy),
    # oraz listę wierzchołków, przez które trzeba przejść, żeby dostać się do danego wierzchołka (i.e. rodziców)
    print("visited vertices, with their travel values from point {}: {}".format(start, visited))
    print("travel paths (list of parents for each vertex):", travel_paths)
    return visited, travel_paths

def generate_path(parents, start, end):
    """
    Funkcja pomocnicza, zwracająca trasę od początkowego do końcowego punktu.
    Wejście:
    parents - lista rodziców każdego wierzchołka
    start - wierzchołek startowy
    end - wierzchołek końcowy
    Wyjście:
    path - trasa od start do end
    """
    # zaczynamy od dodania punktu końcowego do trasy
    path = [end]
    # i teraz magia: patrzymy na rodzica obecnego początku naszej trasy
    # (w pierszyej iteracji nasz początek trasy to punkt końcowy)
    while True:
        key = parents[path[0]]
        # i wstawiamy go na początek trasy
        path.insert(0, key)
        # jeśli rodzic to punkt startowy, to już dotarliśmy, czyli kończymy pętlę
        if key == start:
            break
    print("Path to take from {} to {}: {}".format(start, end, path))
    return path


# poniżej uruchamiamy algorytm z grafem, który ustanowiliśmy na samej górze
# przykładowo tutaj uruchomiłem dla wierzchołka 2
visited, parents = dijkstra(vertices, distances, 2)
# algorytm nam obliczył listę rodziców, czyli możemy wypisywać trasy
generate_path(parents, 2, 3)
generate_path(parents, 2, 5)
generate_path(parents, 2, 12)