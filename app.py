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
learningRate = 0.01
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
            UpdateTheta();
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
    time.sleep(0.5);

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

        x_points = data['km']
        y_points = data['price']

        x_lines = data['km']
        click.echo(click.style(f"\nThetha1 is: {tetha1}, {tetha0}", fg='green'));
        y_lines = tetha1 * x_lines + tetha0;

        plt.figure(figsize=(8,5));   
        plt.scatter(data['km'], data['price']);
        plt.plot(x_lines, y_lines, color='red', linewidth=2);

        plt.title("Price/km Graph");
        plt.xlabel('km');
        plt.ylabel('price');
        
        plt.savefig("figure.png");
        subprocess.run(["xdg-open", "figure.png"]);
        graphOpen = True
        plt.close();
    except:
        click.echo("\nerror");
        return;


# normalized_value = (value - min) / (max - min)

def UpdateTheta():
    global tetha1;
    global tetha0;
    global learningRate;

    data = pd.read_csv("db.csv");
    linesNB = data["km"].count();
    if linesNB < 2:
        return;
    km = data["km"];
    price = data["price"];

    normKm = (km - km.min()) / (km.max() - km.min());
    normPrice = (price - price.min()) / (price.max() - price.min());
    
    nTetha1 = tetha1 * (km.max() - km.min()) / (price.max() - price.min());
    nTetha0 = (tetha0 - price.min()) / (price.max() - price.min()) + (nTetha1 * km.min()) / (km.max() - km.min());

    # click.echo(click.style(f"\nEstimate Price before : {nTetha1, nTetha0}", fg='green'));

    for i in range(1000000):
        oldVal0 = nTetha0;
        oldVal1 = nTetha1;

        sumMarginPriceTheta0 = ((normKm * oldVal1 + oldVal0 - normPrice)).sum();
        nTetha0 = oldVal0 - (learningRate * (1/linesNB) * sumMarginPriceTheta0);

        sumMarginPriceTheta1 = ((normKm * oldVal1 + oldVal0 - normPrice) * normKm).sum();
        nTetha1 = oldVal1 - (learningRate * (1/linesNB) * sumMarginPriceTheta1);

        if abs(nTetha1 - oldVal1) < 0.00001 and abs(nTetha0 - oldVal0) < 0.00001:
            break;
    tetha1 = (price.max() - price.min()) * nTetha1 / (km.max() - km.min());
    tetha0 = price.min() + (price.max() - price.min()) * (nTetha0 - nTetha1 * km.min() / (km.max() - km.min()));
    click.echo(click.style(f"\nTheta is Updated", fg='green'));
    time.sleep(0.5);

# A = (maxPrice - minPrice) * theta1 / (maxKm - minKm)
# B = minPrice + (maxPrice - minPrice) * (theta0 - theta1 * minKm / (maxKm - minKm))


if __name__ == '__main__':
    main()
