let selector = document.querySelector("input[type='tel']");
let im = new Inputmask("+7(999)999-99-99")
im.mask(selector);

new JustValidate('.row-block', {
  rules: {
    name: {
      required: true,
      minLength: 2,
      maxLength: 20,
      strength: {
        custom: '^[а-яА-Я]'
      }
    },
    tel: {
      required: true,
      function: (name, value) => {
        const phone = selector.inputmask.unmaskedvalue()
        return Number(phone) && phone.length === 10
      }
    },
    mail: {
      required: true,
      email: true
    },
  },
  messages: {
    name: {
      required: 'Недопустимый формат',
      minLength: 'Введите 3 и более символов',
      maxLength: 'Введите минимум 20 символов',
      strength: 'Недопустимый формат'
    },
    tel: {
      required: 'Введите 10 символов'
    }
  }
});