import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';

export const useUserStore = defineStore(
  'user',
  () => {
    const API_URL = 'http://127.0.0.1:8000'; // API URL
    const router = useRouter();
    const token = ref(null); // 로그인 토큰
    const loginUsername = ref(null); // 로그인한 사용자 이름

    // 로그인 메서드
    const logIn = function (payload) {
      const { username, password } = payload;

      axios({
        method: 'post',
        url: `${API_URL}/dj-rest-auth/login/`,
        data: {
          username,
          password,
        },
      })
        .then((response) => {
          console.log('response = ', response);
          token.value = response.data.key;
          loginUsername.value = username;

          router.push('/'); // 로그인 성공 후 메인 페이지로 이동
        })
        .catch((error) => {
          console.log('error = ', error);
          alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.');
        });
    };

    // 로그아웃 메서드
    const logOut = async function () {
      try {
        await axios({
          method: 'post',
          url: `${API_URL}/dj-rest-auth/logout/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });

        // 상태 초기화
        token.value = null;
        loginUsername.value = null;
        alert('로그아웃되었습니다.');
        router.push('/'); // 로그아웃 후 메인 페이지로 이동
      } catch (error) {
        console.error('로그아웃 중 오류 발생:', error);
        alert('로그아웃에 실패했습니다. 다시 시도해주세요.');
      }
    };

    // 회원가입 메서드
    const signUp = function (payload) {
      const { username, password1, password2 } = payload;

      axios({
        method: 'post',
        url: `${API_URL}/dj-rest-auth/registration/`,
        data: {
          username,
          password1,
          password2,
        },
      })
        .then((response) => {
          alert('회원가입 성공!');
          logIn({ username, password: password1 });
        })
        .catch((error) => {
          console.log(error);
          alert('회원가입에 실패했습니다. 다시 시도해주세요.');
        });
    };

    return { token, loginUsername, logIn, logOut, signUp };
  },
  { persist: true } // Pinia 상태 유지
);
