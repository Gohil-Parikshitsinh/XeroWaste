document.addEventListener('DOMContentLoaded', function() {
    // Team members data
    const teamMembers = [
      {
        name: "Parikshitsinh Gohil",
        role: "Team Lead"
      },
      {
        name: "Vinay Dhamsaniya",
        role: "AI Engineer"
      },
      {
        name: "Dhairya Gandhi",
        role: "Full Stack Developer"
      },
      {
        name: "Naresh Prajapati",
        role: "UX/UI Designer"
      }
    ];
    
    // Get the container for team members
    const teamContainer = document.getElementById('team-members');
    
    // Populate team members
    teamMembers.forEach(member => {
      const memberCard = document.createElement('div');
      memberCard.className = 'bg-white rounded-lg overflow-hidden shadow-md p-6 text-center';
      
      const nameElement = document.createElement('h3');
      nameElement.className = 'text-xl font-bold mb-1';
      nameElement.textContent = member.name;
      
      const roleElement = document.createElement('p');
      roleElement.className = 'text-green-600 font-medium';
      roleElement.textContent = member.role;
      
      memberCard.appendChild(nameElement);
      memberCard.appendChild(roleElement);
      
      teamContainer.appendChild(memberCard);
    });
  });
  