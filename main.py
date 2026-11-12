from dataclasses import dataclass, field
from drafter import *

# DATA CLASSES
@dataclass
class Reaction:
    reaction_name: str
    reactant_conc: float
    product_conc: float
    kc_value: float

@dataclass
class History:
    reactions: list[Reaction] = field(default_factory=list)
    current_reaction: int = 0
    total_calculations: int = 0
    steps: bool = False

# Initial state
state = History()

# HELPER FUNCTION

def calculate_kc(reactant_conc, product_conc):
    if reactant_conc <= 0:
        return 0
    return product_conc / reactant_conc


# HOME PAGE
@route
def index(state: History) -> Page:
    content = [
        Header("RICE Table and Kc Calculator"),
        Paragraph("Generate RICE tables and calculate equilibrium constants."),
        Button("Create Reaction", "create_reaction"),
        Button("View History", "view_history"),
        Button("About", "about_page")
    ]
    return Page(state, content)

@route
def save_reaction(state: History,
                  reaction_name: str,
                  reactant: str,
                  product: str) -> Page:

    reactant = float(reactant)
    product = float(product)

    kc = calculate_kc(reactant, product)

    new_reaction = Reaction(
        reaction_name,
        reactant,
        product,
        kc
    )

    state.reactions.append(new_reaction)
    state.total_calculations += 1

    return reaction_details(state, len(state.reactions) - 1)

# CREATE REACTION PAGE
@route
def create_reaction(state: History) -> Page:
    content = [
        Header("Create Reaction"),
        "Reaction Name:",
        TextBox("reaction_name"),
        "Reactant Concentration:",
        TextBox("reactant"),
        "Product Concentration:",
        TextBox("product"),
        Button("Calculate", "save_reaction"),
        Button("Home", "index")
    ]
    return Page(state, content)

#DETAILS OF A REACTION
@route
def reaction_details(state: History, index: int) -> Page:
    reaction = state.reactions[index]

    content = [
        Header(reaction.reaction_name),
        Paragraph(f"Reactant concentration: {reaction.reactant_conc}"),
        Paragraph(f"Product concentration: {reaction.product_conc}"),
        Paragraph(f"Kc = {reaction.kc_value}"),
        Button("View History", "view_history"),
        Button("Home", "index")
    ]
    return Page(state, content)

#PREVIOUS REACTIONS
@route
def view_history(state: History) -> Page:
    content = [Header("Reaction History")]

    if len(state.reactions) == 0:
        content.append("No reactions saved.")

    for index, reaction in enumerate(state.reactions):
        content.append(
            Paragraph(f"{index + 1}. {reaction.reaction_name}")
        )

    content.append(
        Paragraph(f"Total Calculations: {state.total_calculations}")
    )
    content.append(Button("Home", "index"))

    return Page(state, content)

# ABOUT PAGE (WEBSITE PURPOSE)
@route
def about_page(state: History) -> Page:
    content = [
        Header("About"),
        Paragraph(
            "This website helps chemistry students "
            "generate simple equilibrium calculations."
        ),
        Paragraph(
            "Users can save reactions and view previous calculations."
        ),
        Button("Home", "index")
    ]
    return Page(state, content)



# START WEBSITE
start_server(initial_state=state)
