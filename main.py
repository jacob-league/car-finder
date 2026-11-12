from drafter import *
from dataclasses import dataclass

set_website_title("Corgi Cafe")
set_site_information(
    author="Your Name",
    description="Order snacks for very good dogs.",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)

# dataclasses

@dataclass
class Service:
    work_done: str
    date: str
    location: str


@dataclass
class Car:
    year: int
    make: str
    model: str
    price: int
    mileage: int
    condition: str
    engine: str
    service_records: list[Service]


@dataclass
class State:
    cars: list[Car]
    search_make: str
    search_model: str
    max_price: int
    selected_car: int
    sort_option: str
    max_mileage: int


# car data

cars = [
    Car(2020, "Ford", "F-150", 28000, 68000,"Good", "3.5L V6", [Service("Oil change", "2024-06-15", "Ford Service Center"),Service("Brake replacement", "2025-02-10", "Auto Repair Shop")]),
    Car(2022, "Toyota", "Camry", 24000, 30000,"Excellent", "2.5L I4", [Service("Oil change", "2025-04-12", "Toyota Service Center")]),
    Car(2018, "Honda", "Civic", 16000, 85000,"Good", "2.0L I4", [Service("Tire replacement", "2024-08-20", "Tire Shop"),Service("Oil change", "2025-01-15", "Honda Service Center")]),
    Car(2021, "Chevrolet", "Silverado", 32000, 45000,"Excellent", "5.3L V8", [Service("Oil change", "2025-03-05", "Chevrolet Service Center")]),
    Car(2019, "Subaru", "WRX", 23000, 55000,"Good", "2.0L Turbo", [Service("Spark plug replacement", "2024-11-10", "Subaru Shop")])
]


# home page

@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Car Finder"),
        Text("Welcome to Car Finder! Find your next car."),
        Div(Link("View Available Cars", view_cars)),
        Div(Link("Search and Filter Cars", search_page))
    ])


# car selection

@route
def select_car_0(state: State) -> Page:
    state.selected_car = 0
    return car_details(state)


@route
def select_car_1(state: State) -> Page:
    state.selected_car = 1
    return car_details(state)


@route
def select_car_2(state: State) -> Page:
    state.selected_car = 2
    return car_details(state)


@route
def select_car_3(state: State) -> Page:
    state.selected_car = 3
    return car_details(state)


@route
def select_car_4(state: State) -> Page:
    state.selected_car = 4
    return car_details(state)


# clickable car links

def make_car_links(state: State, car_indexes: list[int]) -> list:
    results = []

    car_routes = [
        select_car_0,
        select_car_1,
        select_car_2,
        select_car_3,
        select_car_4
    ]

    for i in car_indexes:
        car = state.cars[i]

        results.append(
            Div(Link(f"{car.year} {car.make} {car.model} - ${car.price:,}",car_routes[i]))
        )

    return results


# view cars

@route
def view_cars(state: State) -> Page:
    indexes = []

    for i in range(len(state.cars)):
        indexes.append(i)

    results = make_car_links(state, indexes)

    return Page(state, [
        Header("Available Cars"),
        *results,
        Div(Link("Search and Filter Cars", search_page)),
        Div(Link("Back to Home", index))
    ])


# car details page

@route
def car_details(state: State) -> Page:

    if state.selected_car < 0 or state.selected_car >= len(state.cars):
        return Page(state, [
            Header("No Car Selected"),
            Link("View Available Cars", view_cars)
        ])

    car = state.cars[state.selected_car]

    records = []

    for service in car.service_records:
        records.append(Div(Text(f"Work Done: {service.work_done}")))
        records.append(Div(Text(f"Date: {service.date}")))
        records.append(Div(Text(f"Location: {service.location}")))
        records.append(Div(Text("--------------------")))

    if len(records) == 0:
        records.append(Text("No service records available."))

    return Page(state, [
        Header(f"{car.year} {car.make} {car.model}"),
        Div(Text(f"Price: ${car.price:,}")),
        Div(Text(f"Mileage: {car.mileage:,} miles")),
        Div(Text(f"Condition: {car.condition}")),
        Div(Text(f"Engine: {car.engine}")),
        Header("Service History"),
        *records,
        Div(Link("Back to Available Cars", view_cars)),
        Div(Link("Search Cars", search_page)),
        Div(Link("Back to Home", index))
    ])


# search page 

@route
def search_page(state: State) -> Page:
    return Page(state, [
        Header("Search and Filter Cars"),
        Text("Leave make or model blank to search all."),
        Div(Text("Make:")),
        Div(TextBox("search_make", state.search_make)),
        Div(Text("Model:")),
        Div(TextBox("search_model", state.search_model)),
        Div(Text("Maximum Price ($):")),
        Div(TextBox("max_price", str(state.max_price))),
        Div(Text("Maximum Mileage:")),
        Div(TextBox("max_mileage", str(state.max_mileage))),
        Div(Text("Sort Options:")),
        Text("Enter: None, Price Low, Price High, Mileage Low, Mileage High, Year Newest, Year Oldest"),
        Div(TextBox("sort_option", state.sort_option)),
        Div(Button("Search Cars", search_results)),
        Div(Link("View All Cars", view_cars)),
        Div(Link("Back to Home", index))
    ])


# filter cars

def filter_cars(state: State) -> list[int]:
    matches = []

    for i in range(len(state.cars)):
        car = state.cars[i]

        make_matches = state.search_make.lower() in car.make.lower()
        model_matches = state.search_model.lower() in car.model.lower()
        price_matches = car.price <= state.max_price
        mileage_matches = car.mileage <= state.max_mileage

        if (make_matches and model_matches
                and price_matches and mileage_matches):
            matches.append(i)

    return matches


# sort cars

def sort_cars(state: State, indexes: list[int]) -> list[int]:
    option = state.sort_option.strip().lower()

    if option == "price low":
        return sorted(indexes, key=lambda i: state.cars[i].price)

    elif option == "price high":
        return sorted(indexes,key=lambda i: state.cars[i].price,reverse=True)

    elif option == "mileage low":
        return sorted(indexes, key=lambda i: state.cars[i].mileage)

    elif option == "mileage high":
        return sorted(indexes,key=lambda i: state.cars[i].mileage,reverse=True)

    elif option == "year newest":
        return sorted(indexes,key=lambda i: state.cars[i].year,reverse=True)

    elif option == "year oldest":
        return sorted(indexes, key=lambda i: state.cars[i].year)

    return indexes


# search results page

@route
def search_results(state: State, search_make: str,
                   search_model: str, max_price: str,
                   max_mileage: str, sort_option: str) -> Page:

    state.search_make = search_make.strip()
    state.search_model = search_model.strip()
    state.sort_option = sort_option.strip()

    try:
        price = int(max_price)
        mileage = int(max_mileage)

        if price < 0 or mileage < 0:
            raise ValueError

    except ValueError:
        return Page(state, [
            Header("Invalid Search"),
            Text("Please enter valid nonnegative numbers for price and mileage."),
            Div(Link("Try Again", search_page)),
            Div(Link("Back to Home", index))
        ])

    state.max_price = price
    state.max_mileage = mileage

    matches = filter_cars(state)
    matches = sort_cars(state, matches)

    results = make_car_links(state, matches)

    if len(results) == 0:
        results.append(Text("No cars found matching your search."))

    return Page(state, [
        Header("Search Results"),
        Text(f"Found {len(matches)} matching cars."),
        *results,
        Div(Link("Search Again", search_page)),
        Div(Link("View All Cars", view_cars)),
        Div(Link("Back to Home", index))
    ])


# these are the unit tests for all of the funcs

def run_tests():

    test_state = State(cars, "", "", 50000, -1, "None", 200000)

    # Route 1: Home Page
    assert isinstance(index(test_state), Page)

    # Route 2: View Cars
    assert isinstance(view_cars(test_state), Page)

    # Routes 3-7: Select Cars
    assert isinstance(select_car_0(test_state), Page)
    assert test_state.selected_car == 0

    assert isinstance(select_car_1(test_state), Page)
    assert test_state.selected_car == 1

    assert isinstance(select_car_2(test_state), Page)
    assert test_state.selected_car == 2

    assert isinstance(select_car_3(test_state), Page)
    assert test_state.selected_car == 3

    assert isinstance(select_car_4(test_state), Page)
    assert test_state.selected_car == 4

    # Route 8: Car Details
    test_state.selected_car = 0
    assert isinstance(car_details(test_state), Page)

    test_state.selected_car = -1
    assert isinstance(car_details(test_state), Page)

    # Route 9: Search Page
    assert isinstance(search_page(test_state), Page)

    # Route 10: Search Results
    result = search_results(test_state, "Ford", "F-150","50000", "200000", "None")
    assert isinstance(result, Page)
    assert test_state.search_make == "Ford"
    assert test_state.search_model == "F-150"

    # Search with no matches
    result = search_results(test_state, "BMW", "M3","50000", "200000", "None")
    assert isinstance(result, Page)

    # Invalid price
    result = search_results(test_state, "", "","abc", "200000", "None")
    assert isinstance(result, Page)

    # Negative mileage
    result = search_results(test_state, "", "","50000", "-100", "None")
    assert isinstance(result, Page)

    # Filter by price
    test_state.search_make = ""
    test_state.search_model = ""
    test_state.max_price = 25000
    test_state.max_mileage = 200000
    assert filter_cars(test_state) == [1, 2, 4]

    # Filter by make
    test_state.search_make = "Ford"
    test_state.max_price = 50000
    assert filter_cars(test_state) == [0]

    # Filter by model
    test_state.search_make = ""
    test_state.search_model = "Camry"
    assert filter_cars(test_state) == [1]

    # Filter by mileage
    test_state.search_model = ""
    test_state.max_mileage = 50000
    assert filter_cars(test_state) == [1, 3]

    # Sorting tests
    indexes = [0, 1, 2, 3, 4]

    test_state.sort_option = "Price Low"
    assert sort_cars(test_state, indexes) == [2, 4, 1, 0, 3]

    test_state.sort_option = "Price High"
    assert sort_cars(test_state, indexes) == [3, 0, 1, 4, 2]

    test_state.sort_option = "Mileage Low"
    assert sort_cars(test_state, indexes) == [1, 3, 4, 0, 2]

    test_state.sort_option = "Mileage High"
    assert sort_cars(test_state, indexes) == [2, 0, 4, 3, 1]

    test_state.sort_option = "Year Newest"
    assert sort_cars(test_state, indexes) == [1, 3, 0, 4, 2]

    test_state.sort_option = "Year Oldest"
    assert sort_cars(test_state, indexes) == [2, 4, 0, 3, 1]

    test_state.sort_option = "None"
    assert sort_cars(test_state, indexes) == indexes

    # Car link tests
    assert len(make_car_links(test_state, [0, 1])) == 2
    assert len(make_car_links(test_state, [])) == 0

    # Service record data test
    assert len(cars[0].service_records) == 2
    assert cars[0].service_records[0].work_done == "Oil change"

    print("All Car Finder tests passed!")


#runs test and starts the website 

if __name__ == "__main__":
    run_tests()

    start_server(State(cars, "", "", 50000, -1, "None", 200000))


