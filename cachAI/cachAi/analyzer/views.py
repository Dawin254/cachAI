import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
import os

def analyze_logs(request):
    # Load dataset from the data folder
    file_path = os.path.join(settings.BASE_DIR, 'analyzer/data/user_logs.csv')
    data = pd.read_csv(file_path)
    
    # Analyze the data
    freq_data = data.groupby(['content_id', 'content_type', 'source']).size().reset_index(name='access_count')
    freq_data = freq_data.sort_values(by='access_count', ascending=False)
    freq_data = freq_data.head(50)


    # Plot the frequently accessed content
    plot_file = os.path.join(settings.BASE_DIR, 'analyzer/static/freq_content.png')
    top_data = freq_data.head(10000)
    plt.figure(figsize=(10, 6))
    plt.bar(top_data['content_id'], top_data['access_count'], color='skyblue')
    plt.title('Top 10 Frequently Accessed Content')
    plt.xlabel('Content ID')
    plt.ylabel('Access Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()

    # Send data to template
    return render(request, 'index.html', {
        'freq_data': freq_data.to_dict(orient='records'),
        'plot_path': '/static/freq_content.png',
    })
