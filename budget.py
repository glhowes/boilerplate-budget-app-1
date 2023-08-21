category_names = list()

class Category:

    def __init__(self, category_name):
        self.category_name = category_name
        self.balance = 0
        self.ledger = list()
        if category_name not in category_names:
          category_names.append(category_name)

    def __repr__(self):
        self.header = str(self.category_name).center(30, "*")
        self.body = str()
        self.footer = f"\nTotal: {str(self.balance)}"
        for entry in self.ledger:
            self.dict = entry
            self.desc = entry.get("description")
            self.val = "{:.2f}".format(float(entry.get("amount")))
            self.body += f"\n{self.desc[:23]}{(str(self.val))[:7].rjust(30 - (len(self.desc[:23])))}"
            self.string = f"{self.header}{self.body}{self.footer}"
        return self.string

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        self.balance = round(self.balance, 2)
        return self.balance
    
    def transfer(self, amount, category_instance):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category_instance.category_name}")
            category_instance.deposit(amount, f"Transfer from {self.category_name}")
            return True
        else:
            return False

    def check_funds(self, amount):
        if (self.balance - amount) >= 0:
            return True
        else:
            return False



def create_spend_chart(categories):
    
    spent_lst = []
    cat_lst = list()
    for category in categories:
        cat_lst.append(category.category_name)
        category = category.ledger
        spent = 0
        for num in range(len(category)):
            if float(category[num].get("amount")) < 0:
                spent += -1 * float(((category[num].get("amount"))))
        spent_lst.append(spent)

    total_spent = sum(spent_lst)
    percent_lst = list()

    for percent in spent_lst:
      percent_lst.append(int(100*percent/total_spent))

    header = "Percentage spent by category\n"
    body = str()
    
    for ten in range(100, -1, -10):
        body += f"{str(ten).rjust(3)}|"
        for z in range(len(percent_lst)):
            if z == 0:
                if ten <= percent_lst[z]:
                    body += " o"
                else:
                    body += "  "
            elif z == (len(percent_lst) - 1):
                if ten <= percent_lst[z]:
                    body += "  o  "
                else:
                    body += "     "
            else:
                if ten <= percent_lst[z]:
                    body += "  o"
                else:
                    body += "   "
        body += "\n"

    base = str()

    longest_name = 0
    for name in cat_lst:
        if len(name) > longest_name:
            longest_name = len(name)

    base += "    "+(len(cat_lst) * "---")+"-\n"

    for i in range(longest_name):
        base += "     "
        for name in cat_lst:
            if len(name) >= (i+1):
                base += f"{name[i]}  "
            else:
                base += "   "
        if i == (longest_name - 1):
          base += ""
        else:
          base += "\n"
    spend_chart = f"{header}{body}{base}"
    return spend_chart