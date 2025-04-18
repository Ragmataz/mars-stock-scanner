from scanner.fetch_data import get_data, get_nse500_list, get_index_symbol
from scanner.mars import calculate_mars_signal
from scanner.telegram import send_telegram_message

def main():
    stock_list = get_nse500_list()
    index_symbol = get_index_symbol()
    data = get_data(stock_list, index_symbol)

    results = calculate_mars_signal(data)
    if results:
        send_telegram_message(results)
    else:
        print("No signals today.")

if __name__ == "__main__":
    main()
