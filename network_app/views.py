from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Person, Connection
from .forms import PersonForm, ConnectionForm  # Add this import
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def index(request):
    """Main view to display the network"""
    people = Person.objects.all()
    connections = Connection.objects.all()
    return render(request, 'network_app/index.html', {
        'people': people,
        'connections': connections,
    })

# Add these new view functions:

def add_person(request):
    """Handle adding new people to the network"""
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            messages.success(request, f'Successfully added {person.name} to the network!')
            return redirect('index')  # Redirect to home page after success
    else:
        form = PersonForm()
    
    return render(request, 'network_app/add_person.html', {'form': form})

def add_connection(request):
    """Handle creating new connections between people"""
    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ConnectionForm()
    return render(request, 'network_app/add_connection.html', {'form': form})

def view_network(request):
    # Create a new graph
    G = nx.Graph()
    
    # Add nodes (persons)
    persons = Person.objects.all()
    for person in persons:
        G.add_node(person.name)
    
    # Add edges (connections)
    connections = Connection.objects.all()
    for conn in connections:
        # Add edge with connection strength as weight
        G.add_edge(conn.person_from.name, conn.person_to.name, 
                  weight=conn.strength,
                  connection_type=conn.connection_type)
    
    # Create the visualization
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=500)
    
    # Draw edges with different colors based on connection type
    edge_colors = {'friend': 'green', 'family': 'red', 
                  'colleague': 'blue', 'other': 'gray'}
                  
    for edge in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, 
                             edgelist=[(edge[0], edge[1])],
                             edge_color=edge_colors[edge[2]['connection_type']],
                             width=edge[2]['weight'])
    
    # Add labels
    nx.draw_networkx_labels(G, pos)
    
    # Save plot to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Encode the image to base64
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return render(request, 'network_app/view_network.html', 
                 {'graphic': graphic})

def mock_view_network(request):
    G = nx.Graph()
    
    # Get actual data from database
    persons = Person.objects.all()
    connections = Connection.objects.all()
    
    # Add nodes
    for person in persons:
        G.add_node(person.name)
    
    # Add edges
    for conn in connections:
        G.add_edge(conn.person_from.name, 
                  conn.person_to.name,
                  connection_type=conn.connection_type,
                  weight=conn.strength)
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, 
                          node_color='lightblue',
                          node_size=500)
    
    # Draw edges
    edge_colors = {
        'friend': 'green',
        'family': 'red',
        'colleague': 'blue',
        'other': 'gray'
    }
    
    for edge in G.edges(data=True):
        nx.draw_networkx_edges(G, pos,
                             edgelist=[(edge[0], edge[1])],
                             edge_color=edge_colors[edge[2]['connection_type']],
                             width=edge[2]['weight'])
    
    # Add labels
    nx.draw_networkx_labels(G, pos)
    
    # Save plot
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    return render(request, 'network_app/view_network.html',
                 {'graphic': graphic})

def add_sample_people(request):
    # Sample data
    sample_people = [
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'profession': 'Software Engineer',
            'interests': 'Programming, Gaming'
        },
        {
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'profession': 'Data Scientist',
            'interests': 'AI, Machine Learning'
        },
        {
            'name': 'Mike Johnson',
            'email': 'mike@example.com',
            'profession': 'Designer',
            'interests': 'UI/UX, Art'
        }
    ]

    # Add people to database
    for person_data in sample_people:
        person, created = Person.objects.get_or_create(
            email=person_data['email'],
            defaults=person_data
        )
        if created:
            messages.success(request, f"Added {person.name} to the network")

    # Add sample connections
    connections = [
        ('john@example.com', 'jane@example.com', 'colleague', 4),
        ('jane@example.com', 'mike@example.com', 'friend', 3),
        ('mike@example.com', 'john@example.com', 'other', 2),
    ]

    for from_email, to_email, conn_type, strength in connections:
        person_from = Person.objects.get(email=from_email)
        person_to = Person.objects.get(email=to_email)
        Connection.objects.get_or_create(
            person_from=person_from,
            person_to=person_to,
            defaults={
                'connection_type': conn_type,
                'strength': strength
            }
        )

    messages.success(request, "Sample network created successfully!")
    return redirect('mock_network')