import axios from "axios";

// const BASE_URL = "http://localhost:8000/api";

const BASE_URL = import.meta.env.VITE_API_URL;


// Helper function to get access token
const getAccessToken = () => localStorage.getItem("accessToken");

// Helper function to refresh token if needed
export const getRefreshToken = async () => {

  const refreshToken = localStorage.getItem("refreshToken");
  // if (!refreshToken) {
  //   throw new Error("No refresh token found. Please log in again.");
  // }
  // if (refreshToken){
  try {
    const response = await axios.post(`${BASE_URL}/login/refresh/`, { refresh: refreshToken });

    const newAccessToken = response.data.access;
    localStorage.setItem("accessToken", newAccessToken);
    console.log("access token",newAccessToken)
    return newAccessToken; //  Return the new token
  } catch (error) {
    console.error("Token refresh failed:", error);
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");

    // throw new Error("Session expired. Please log in again.");
  }
// }
};


// Axios instance with interceptors
const api = axios.create({
  baseURL: BASE_URL,
});



let isRefreshing = false;
let refreshSubscribers = [];

// Function to add subscribers (requests waiting for a new token)
function onTokenRefreshed(newToken) {
  refreshSubscribers.forEach((callback) => callback(newToken));
  refreshSubscribers = [];
}

// Request Interceptor: Attach Access Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle Token Expiry
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not retrying yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // If already refreshing, queue the request to be retried later
        return new Promise((resolve) => {
          refreshSubscribers.push((newToken) => {
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            resolve(api(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const newAccessToken = await getRefreshToken();
        localStorage.setItem("accessToken", newAccessToken);

        // Notify all queued requests to retry with new token
        onTokenRefreshed(newAccessToken);

        isRefreshing = false;
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest); // Retry failed request
      } catch (refreshError) {
        isRefreshing = false;
        console.error("Session expired. Please log in again.");
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);





// api.interceptors.request.use(
//   (config) => {
//   const token = localStorage.getItem('accessToken');
//   if (token) {
//   config.headers.Authorization = `Bearer ${token}`;
//   }
//   return config;
//   },
//   (error) => Promise.reject(error)
//   );


// api.interceptors.response.use(
//    (response) => response,
//    async (error) => {
//     const originalRequest = error.config;

//     if (error.response?.status === 401 && !originalRequest._retry) {
//      originalRequest._retry = true;
//      try {
//       const newAccessToken = await getRefreshToken();
//       originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
//       return api(originalRequest);
//      } catch (refreshError) {
//       console.error('Session expired. Please log in again.');
//       return Promise.reject(refreshError);
//      }
//     }

//     return Promise.reject(error);
//    }
//   );



// Signup API
export const signup = (email, first_name, last_name, password, repassword, organization) =>
  api.post("/signup/", { email, first_name, last_name, password, repassword, organization });

// Login API
export const login = (email, password) => api.post("/login/", { email, password });

// Get organizations
export const getOrganizations = async () => {
  try {
    const response = await api.get("/organization/list/");
    return response.data;
  } catch (error) {
    console.error("Error fetching organizations:", error);
    throw error;
  }
};

// Get user
export const getUser = () =>
  api.get("/users/", { headers: { Authorization: `Bearer ${getAccessToken()}` } });

// Logout API
export const logout = async () => {
  try {
    await api.post("/logout/", { refresh: localStorage.getItem("refreshToken") }, {
      headers: { Authorization: `Bearer ${getAccessToken()}` },
    });
  } catch (error) {
    console.error("Failed to logout:", error);
  }
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
};

// Reset password
export const resetPassword = (oldPassword, newPassword, confirmPassword) =>
  api.put("/reset-password/", {
    old_password: oldPassword,
    new_password: newPassword,
    confirm_password: confirmPassword,
    refresh_token: localStorage.getItem("refreshToken"),
  });

// Give Kudos
export const giveKudos = (receiverEmail, message) =>
  api.post("/kudos/give/", { receiver: receiverEmail, message }, {
    headers: { Authorization: `Bearer ${getAccessToken()}` },
  });

// Get Kudos
export const getKudos = () =>
  api.get("/kudos/", { headers: { Authorization: `Bearer ${getAccessToken()}` } });

// Get Latest Kudos
export const getLatestKudos = () =>
  api.get("/latestkudos/", { headers: { Authorization: `Bearer ${getAccessToken()}` } });


// get kudos count balance
export const getkudoscount = async () => {
  try {
    const response = await api.get("/kudosremaining", {
      headers: { Authorization: `Bearer ${getAccessToken()}` },
    });
    return response.data
  } catch (error) {
    console.error("Error fetching Kudos count:", error);
    throw error;
  }

};


















// import axios from "axios";
// const BASE_URL = "http://localhost:8000/api";

// // signup API function

// export const signup = async (email,first_name,last_name, password, repassword, organization) => {
//   return axios.post(`${BASE_URL}/signup/`, {
//     email,
//     first_name,
//     last_name,
//     password,
//     repassword,
//     organization,
//   });
// };



// // login API function

// export const login = async (email, password) => {
//   return axios.post(`${BASE_URL}/login/`, {
//     email,
//     password,
//   });
// };


// // get organizations API function

// export const getOrganizations = async () => {
//   try {
//     const response = await axios.get(`${BASE_URL}/organization/list/`);
//     return response.data; // Assuming the API returns a list of organizations
//   } catch (error) {
//     console.error("Error fetching organizations:", error);
//     throw error;
//   }
// };


// // get user  API function

// export const getUser = async () => {
//   let token = localStorage.getItem("accessToken"); // Get token from localStorage

//   // if (!token) {
//   //   try {
//   //     token = await getRefreshToken(); // Get a new token if expired
//   //   } catch (error) {
//   //     console.error("Token refresh failed. Please log in again.");
//   //     throw error;
//   //   }
//   // }

//   return axios.get(`${BASE_URL}/users/`, {
//     headers: {
//       Authorization: `Bearer ${token}`, // Set token in request header
//     },
//   });
// }


// // get refresh token API function
// export const getRefreshToken = async () => {
//   const refreshToken = localStorage.getItem("refreshToken");
//   if (!refreshToken) {
//     throw new Error("No refresh token found. Please log in again.");
//   }

//   try {
//     const response = await axios.post(`${BASE_URL}/login/refresh/`, { refresh: refreshToken });
//     localStorage.setItem("accessToken", response.data.access);
//     console.log("Access Token after refresh:", response.data.access);
//     return response.data.access;
//   } catch (error) {
//     console.error("Failed to refresh token:", error);
//     localStorage.removeItem("accessToken");
//     localStorage.removeItem("refreshToken");
//     throw new Error("Session expired. Please log in again.");
//   }
// };

// setInterval(() => {
//   getRefreshToken();
// }, 2 * 60 * 1000); // Refresh token every 2 minutes


// // logout API function
// export const logout = async () => {
//   try {
//     const refreshToken = localStorage.getItem("refreshToken");

    // if (!refreshToken) {
    //   console.warn("No active session found.");
    //   localStorage.removeItem("accessToken");
    //   localStorage.removeItem("refreshToken");
    //   return;
    // }

    // let accessToken = localStorage.getItem("accessToken");
    // console.log("access token before refresh", accessToken);
    // Try refreshing the token if accessToken is not available
    // if (!accessToken) {
    //   try {
    //     accessToken = await getRefreshToken();
    //     console.log("Access Token after refresh:", accessToken);
    //   } catch (refreshError) {
    //     console.warn("Token refresh failed. Logging out...");
    //     localStorage.removeItem("accessToken");
    //     localStorage.removeItem("refreshToken");
    //     return;
    //   }
    // }

    // Proceed with logout if we have a valid accessToken
    // try {
    //   const response = await axios.post(`${BASE_URL}/logout/`, { refresh: refreshToken }, {
    //     headers: { Authorization: `Bearer ${accessToken}` }
    //   });
    //   return response.data;
    // } catch (error) {
    //   console.error("Failed to logout:", error);
    //   localStorage.removeItem("accessToken");
    //   localStorage.removeItem("refreshToken");
    //   throw new Error("Failed to logout. Please try again.");



      // if (error.response && error.response.status === 401) {
      //   try {
      //     accessToken = await getRefreshToken();
      //     const retryResponse = await axios.get(`${BASE_URL}/kudos/`, {
      //       headers: { Authorization: `Bearer ${accessToken}` },
      //     });
      //     return retryResponse.data;
      //   } catch (refreshError) {
      //     console.error("Token refresh failed, logging out...");
      //     localStorage.removeItem("accessToken");
      //     localStorage.removeItem("refreshToken");
      //     throw new Error("Session expired. Please log in again.");
      //   }
      // } else {
      //   throw error; // Handle other errors
      // }

//     }
//   } catch (error) {
//     console.error("Unexpected error during logout:", error);
//   }
// };





// // reset password API function

// export const resetPassword = async (oldPassword, newPassword, confirmPassword) => {
//   const token = localStorage.getItem("accessToken"); // Get token from localStorage
//   const refreshToken = localStorage.getItem("refreshToken"); // Get refresh token from localStorage
//   // if (!token) {
//   //   token = await getRefreshToken(); // Get a new token if expired
//   // }
//   return axios.put(
//     `${BASE_URL}/reset-password/`,
//     { old_password: oldPassword, new_password: newPassword, confirm_password: confirmPassword ,refresh_token: refreshToken},
//     {
//       headers: {
//         Authorization: `Bearer ${token}`, // Set token in request header
//         "Content-Type": "application/json",
//       },
//     }
//   );
// };


// // give kudos API function
// export const giveKudos = async (receiverEmail, message) => {
//   let token = localStorage.getItem("accessToken"); // Get token from localStorage

//   // if (!token) {
//   //   try {
//   //     token = await getRefreshToken(); // Get a new token if expired
//   //   } catch (error) {
//   //     console.error("Token refresh failed. Please log in again.");
//   //     throw error;
//   //   }
//   // }

//   return axios.post(
//     `${BASE_URL}/kudos/give/`,
//     { receiver: receiverEmail, message: message },
//     {
//       headers: {
//         Authorization: `Bearer ${token}`, // Set token in request header
//         "Content-Type": "application/json",
//       },
//     }
//   );
// };


// // get kudos API function
// export const getKudos = async () => {
//   let token = localStorage.getItem("accessToken"); // Get token from localStorage

//   // if (!token) {
//   //   try {
//   //     token = await getRefreshToken(); // Get a new token if expired
//   //   } catch (error) {
//   //     console.error("Token refresh failed. Please log in again.");
//   //     throw error;
//   //   }
//   // }

//   return axios.get(`${BASE_URL}/kudos/`, {
//     headers: {
//       Authorization: `Bearer ${token}`, // Set token in request header
//     },
//   });
// };


// // get latest kusos API function

// export const getLatestKudos = async () => {
//   let token = localStorage.getItem("accessToken"); // Get token from localStorage

//   // if (!token) {
//   //   try {
//   //     token = await getRefreshToken(); // Get a new token if expired
//   //   } catch (error) {
//   //     console.error("Token refresh failed. Please log in again.");
//   //     throw error;
//   //   }
//   // }

//   return axios.get(`${BASE_URL}/latestkudos/`, {
//     headers: {
//       Authorization: `Bearer ${token}`, // Set token in request header
//     },
//   });
// }
