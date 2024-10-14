import csv

def read_logged_messages(log_file_path):
    messages = {}
    with open(log_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['username']
            message = row['message']
            if username in messages:
                messages[username].append(message)
            else:
                messages[username] = [message]
    return messages

def main():
    log_file_path = 'message_log.csv'
    output_file_path = 'unread_messages.csv'
    
    # Read the logged messages
    messages = read_logged_messages(log_file_path)
    
    # Write unread messages to the output CSV file
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'unread_messages'])
        
        for username, msgs in messages.items():
            writer.writerow([username, msgs])
    
    # Print unread messages to the terminal
    for username, msgs in messages.items():
        print(f'Unread messages for {username}:')
        for msg in msgs:
            print(msg)
        print('---')

if __name__ == '__main__':
    main()
