import requests





var content = new FormUrlEncodedContent(new Dictionary<string, string> { {"client_id", configuration["Security:Auth0:ClientId"] }, {"client_secret", configuration["Security:Auth0:ClientSecret"] }, {"grant_type", "password"}, {"username", HttpContext.Request.Form["username"]}, {"password",HttpContext.Request.Form["password"]} }); var response = await _httpClient.PostAsync($"https://{configuration["Security:Auth0:Domain"]}/oauth/token", content);