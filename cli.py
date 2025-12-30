import click
import time
from click.testing import CliRunner
from InquirerPy import inquirer
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from newData import newData

tetha0 = 0
tetha1 = 0
graphOpen = False

@click.command()

def main():
    createDBFile();
    try:
        while True:
            choice = selectMenu()
            if choice == "Estimate Price":
                estimation()
            elif choice == "New Data":
                newData()
            elif choice == "Graph":
                createGraph()
            elif choice == "Quit":
                break
            UpdateTheta0();
            UpdateTheta1();
    except KeyboardInterrupt:
        print("\n...Leaving....");
    except click.exceptions.Abort:
        print("\n...Leaving....");

def createDBFile():
    with open("db.csv", "w") as f:
        f.write('km,price\n');

def estimation():
    mileage = click.prompt("Enter Mileage", type = float);
    estimatePrice = mileage * tetha1 + tetha0;
    click.echo(click.style(f"\nEstimate Price for the car is: {estimatePrice}", fg='green'));
    time.sleep(1.5);

def selectMenu():
    return inquirer.select(
        message="\n\nYour choice ?",
        choices=["Estimate Price", "New Data", "Graph", "Quit"]
    ).execute()

def createGraph():
    try:
        global tetha0;
        global tetha1;
        data = pd.read_csv("db.csv");
        plt.scatter(data['price'], data['km']);
        plt.title("Price/km Graph");
        plt.xlabel('km');
        plt.ylabel('price');
        plt.magma();
        plt.hist2d
        x = data['price']
        y = tetha1 * x + tetha0;
        click.echo(click.style(f"\nThetha1 is: {tetha1},, {tetha0}", fg='green'));
        plt.plot(x, y, color='red', linewidth=2)
        plt.savefig("figure.png");
        subprocess.run(["xdg-open", "figure.png"])
        graphOpen = True
    except:
        click.echo("\nerror");
        return;

def UpdateTheta1():
    global tetha1;
    data = pd.read_csv("db.csv");
    sumXY = (data["price"] * data["km"]).sum();
    sumX = data["price"].sum();
    sumY = data["km"].sum();
    sumXX = (data["price"] * data["price"]).sum();
    linesNB = data["price"].count();
    tetha1 =  (linesNB * sumXY - sumX * sumY) / (linesNB * sumXX - (sumX * sumX));

def UpdateTheta0() :
    global tetha0;
    data = pd.read_csv("db.csv");
    sumX = data["price"].sum();
    sumY = data["km"].sum();
    linesNB = data["km"].count();
    tetha0 = (sumY - tetha1 * sumX) / linesNB;
    time.sleep(1.5);


if __name__ == '__main__':
    main()
