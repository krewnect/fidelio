const campaigns = [
  {
    id: '59daaf50-5a20-4da5-98a3-3d5a8bca528e',
    name: 'Nueva Campaña',
    type: 'stamps',
    created_at: '2026-08-18T03:21:11.824066+00:00'
  },
  {
    id: 'e60d7473-8a73-4bb4-b296-5184e01fc2f2',
    name: 'Restaurante Demo Rewards',
    type: 'stamps',
    created_at: '2026-08-17T14:22:24.36975+00:00'
  }
];

const filtered = campaigns.filter(c => !['membership', 'multipass', 'certificates'].includes(c.type));
console.log(filtered.length);
