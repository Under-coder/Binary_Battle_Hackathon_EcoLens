# ecolens_api.py
import requests

class EcoLensAPI:
    """
    Simple API wrapper to interact with the EcoLens backend.
    Example usage:
        api = EcoLensAPI(base_url="https://your-backend.onrender.com")
        response = api.get_ecosystem_analysis("Bhopal")
    """

    def __init__(self, base_url: str):
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url

    def get_ecosystem_analysis(self, city: str):
        """
        Call the ecosystem analysis endpoint.
        Returns the JSON response as a Python dict.
        """
        url = f"{self.base_url}/ecosystem-analysis"
        params = {"city": city}
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {e}"}

    def health_check(self):
        """
        Optional: check if the backend is running
        """
        url = f"{self.base_url}/"
        try:
            response = requests.get(url, timeout=10)
            return {"status": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": f"Health check failed: {e}"}

# Example standalone test
if __name__ == "__main__":
    api = EcoLensAPI("http://127.0.0.1:8000")  # change to Render URL after deployment
    print(api.health_check())
    print(api.get_ecosystem_analysis("Bhopal"))
