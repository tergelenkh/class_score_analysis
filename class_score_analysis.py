def read_data(filename):
    # Read `filename` as a list of integer numbers
    data = []
    with open(filename, 'r') as f:
        for line in f:
            # Skip header line starting with '#'
            if line.startswith('#'):
                continue
            try:
                # Split the line by comma and convert to integers
                midterm, final = map(int, line.strip().split(','))
                data.append((midterm, final))  # Append tuple (midterm, final)
            except ValueError:
                print(f"Warning: Skipping malformed line: {line.strip()}")
            except Exception as e:
                print(f"Error: {e} occurred while processing line: {line.strip()}")
    return data

def calc_weighted_average(data_2d, weight):
    # Calculate the weighted averages of each row of `data_2d`
    average = []
    for midterm, final in data_2d:
        avg = midterm * weight[0] + final * weight[1]
        average.append(avg)
    return average

def analyze_data(data_1d):
    # Derive summary of the given `data_1d`
    n = len(data_1d)
    if n == 0:  # Handle case with no data to avoid division by zero
        return 0, 0, 0, 0, 0
    
    # Mean calculation
    mean = sum(data_1d) / n

    # Variance calculation
    var = sum((x - mean) ** 2 for x in data_1d) / n

    # Median calculation
    sorted_data = sorted(data_1d)
    if n % 2 == 0:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        median = sorted_data[n // 2]

    return mean, var, median, min(data_1d), max(data_1d)

if __name__ == '__main__':
    # Read data from CSV
    data = read_data('python02_lab/data/class_score_en.csv')

    if data and len(data[0]) == 2:  # Check if data is valid
        # Calculate weighted averages
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Average |\n')
            report.write('| ------- | ----- | ------- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            # Examination Analysis
            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            
            # For each column (Midterm, Final, Average), write the analysis
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')
