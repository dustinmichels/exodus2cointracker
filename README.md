# Exodus2CoinTracker

If you...
- Are interested in cryptocurrencies
- Use the [Exodus](https://www.exodus.io/) wallet
to hold/exchange tokens
- Use the [CoinTracker](https://www.cointracker.io) website
to track/manage your spending/investing

Then... *boy oh boy is this the script for you!*

Use it to convert a csv you can export of your Exodus transactions into a csv you can import into cointracker

## Usage

1. Git clone and cd into this directory

  ```bash
  # download dir
  git clone https://github.com/dustinmichels/exodus2cointracker.git

  # change dir
  cd exodus2cointracker
  ```

2. Export full CSV from Exodus
  `Exodus > Developer > Export Safe Report Data`

3. Unzip that file into your current directory
  ```bash
  unzip /Users/<username>/Desktop/exodus-exports/exodus-report-SAFE-2018-07-12_12-36-25.zip
  ```

4. Run the python script
  ```bash
  python3 exodus2cointracker.py
  ```

5. Import the csv `cointracker_output.csv` to CoinTracker
