import click
from InquirerPy import inquirer
import time
import pandas as pd

def newData():
    choice = selectData();

    if choice == "Estimate Price":
        return;
    
    match (choice):
        case "Unique data":
            uniqueData();
        case "Data file":
            dataFile();

def selectData():
    return inquirer.select(
        message="\n\nFormat to enter data?",
        choices=["Unique data", "Data file", "Cancel"]
    ).execute();

def uniqueData():
    price = click.prompt("\nEnter Price", type = float);
    mileage = click.prompt("Enter Mileage", type = float);
    if click.confirm(f"\nConfirmation Price: {price}, mileage: {mileage}"):
        try:
            d = {'km': mileage, 'price': price}
            new_row = pd.DataFrame([d])
            data = pd.read_csv("db.csv")
            data = pd.concat([data, new_row])
            data.to_csv("db.csv", index=False)

            click.echo(click.style(f"\nUpdated", fg='green'));
        except FileNotFoundError:
            click.echo(click.style("\nFile not Found", fg='red'));
        time.sleep(1.5);
    else:
        click.echo(click.style(f"\nCancel", fg='red'));
    time.sleep(1.5);

def dataFile():
    fileName = click.prompt("\nName of File")
    try:
        data = pd.read_csv(fileName);
        data.to_csv("db.csv", mode='a',index=False, header=False)
        # UpdateTheta1();
    except FileNotFoundError:
        click.echo(click.style("\nFile not Found", fg='red'));
        time.sleep(1.5);