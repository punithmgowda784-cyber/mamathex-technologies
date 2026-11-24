const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
  });
  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      menuToggle.setAttribute("aria-expanded", "false");
    });
  });
}

const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

const contactForm = document.getElementById("contactForm");
if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(contactForm);
    const subject = encodeURIComponent(`Website enquiry: ${data.get("interest")}`);
    const body = encodeURIComponent(
      `Name: ${data.get("name")}\nEmail: ${data.get("email")}\nInterest: ${data.get("interest")}\n\nMessage:\n${data.get("message")}`
    );
    const status = document.getElementById("formStatus");
    if (status) status.textContent = "Opening your email app to send this enquiry...";
    window.location.href = `mailto:mamathextechno@gmail.com?subject=${subject}&body=${body}`;
  });
}

const BACKEND_URL = "https://YOUR-RENDER-SERVICE.onrender.com";

const contactForm = document.getElementById("contactForm");

if (contactForm) {
    contactForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const button = contactForm.querySelector(
            'button[type="submit"]'
        );

        const status = document.getElementById("formStatus");

        const formData = new FormData(contactForm);

        const enquiry = {
            name: formData.get("name"),
            email: formData.get("email"),
            interest: formData.get("interest"),
            message: formData.get("message")
        };

        button.disabled = true;
        button.textContent = "Sending...";

        try {
            const response = await fetch(
                `${BACKEND_URL}/api/enquiry`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(enquiry)
                }
            );

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.message);
            }

            status.textContent = result.message;
            contactForm.reset();

        } catch (error) {
            status.textContent =
                error.message || "Something went wrong.";
        } finally {
            button.disabled = false;
            button.innerHTML =
                'Prepare enquiry <span>↗</span>';
        }
    });
}
