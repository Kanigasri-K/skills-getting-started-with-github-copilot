document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const signupForm = document.getElementById("signup-form");
  const unregisterForm = document.getElementById("unregister-form");
  const signupActivitySelect = document.getElementById("activity");
  const unregisterActivitySelect = document.getElementById("unregister-activity");
  const messageDiv = document.getElementById("message");

  // Function to display messages
  function showMessage(text, type = "info") {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.classList.remove("hidden");
    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities", { cache: "no-store" });
      const activities = await response.json();

      // Clear loading message and select dropdowns
      activitiesList.innerHTML = "";
      signupActivitySelect.innerHTML = `<option value="">-- Select an activity --</option>`;
      unregisterActivitySelect.innerHTML = `<option value="">-- Select an activity --</option>`;

      // Populate activities list and form options
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        const participantList = document.createElement("ul");
        participantList.className = "participant-list";

        if (details.participants.length > 0) {
          details.participants.forEach((participant) => {
            const listItem = document.createElement("li");
            listItem.className = "participant-item";

            // Participant email span
            const emailSpan = document.createElement("span");
            emailSpan.textContent = participant;
            emailSpan.className = "participant-email";

            // Delete icon
            const deleteBtn = document.createElement("button");
            deleteBtn.className = "delete-participant-btn";
            deleteBtn.title = `Unregister ${participant}`;
            deleteBtn.innerHTML = "&#128465;"; // Trash can emoji
            deleteBtn.addEventListener("click", async (e) => {
              e.preventDefault();
              deleteBtn.disabled = true;
              try {
                const response = await fetch(
                  `/activities/${encodeURIComponent(name)}/unregister?email=${encodeURIComponent(participant)}`,
                  { method: "POST" }
                );
                const result = await response.json();
                if (response.ok) {
                  showMessage(result.message, "success");
                  await fetchActivities();
                } else {
                  showMessage(result.detail || "An error occurred", "error");
                  deleteBtn.disabled = false;
                }
              } catch (error) {
                showMessage("Failed to unregister. Please try again.", "error");
                deleteBtn.disabled = false;
              }
            });

            listItem.appendChild(emailSpan);
            listItem.appendChild(deleteBtn);
            participantList.appendChild(listItem);
          });
        } else {
          const listItem = document.createElement("li");
          listItem.textContent = "No students registered yet.";
          participantList.appendChild(listItem);
        }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <p><strong>Registered Students:</strong></p>
        `;

        activityCard.appendChild(participantList);
        activitiesList.appendChild(activityCard);

        const signupOption = document.createElement("option");
        signupOption.value = name;
        signupOption.textContent = name;
        signupActivitySelect.appendChild(signupOption);

        const unregisterOption = document.createElement("option");
        unregisterOption.value = name;
        unregisterOption.textContent = name;
        unregisterActivitySelect.appendChild(unregisterOption);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle sign-up form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = signupActivitySelect.value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        signupForm.reset();
        await fetchActivities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to sign up. Please try again.", "error");
      console.error("Error signing up:", error);
    }
  });

  // Handle unregister form submission
  unregisterForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("unregister-email").value;
    const activity = unregisterActivitySelect.value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        unregisterForm.reset();
        await fetchActivities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to unregister. Please try again.", "error");
      console.error("Error unregistering:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
