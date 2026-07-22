// Ingredient Taxonomy and Bilingual Categorization Matrix

export const INGREDIENT_CATEGORIES = [
  {
    id: 'dairy_paneer',
    name: 'Paneer, Dairy & Cheese',
    tags: [
      { name: 'Paneer (Cottage Cheese)', varieties: ['Paneer', 'Cottage Cheese', 'Indian Cottage Cheese', 'Chenna'] },
      { name: 'Dahi (Yogurt / Curd)', varieties: ['Plain Dahi', 'Curd', 'Greek Yogurt', 'Flavored Yogurt'] },
      { name: 'Ghee & Butter', varieties: ['Desi Ghee', 'Clarified Butter', 'Unsalted Butter', 'Fresh Butter'] },
      { name: 'Cheese Varieties', varieties: ['Cheddar', 'Mozzarella', 'Parmesan', 'Feta', 'Ricotta'] }
    ]
  },
  {
    id: 'spices_masala',
    name: 'Indian Spices & Masalas',
    tags: [
      { name: 'Haldi (Turmeric)', varieties: ['Turmeric Powder (Haldi)', 'Raw Turmeric', 'Ground Turmeric'] },
      { name: 'Jeera (Cumin Seeds)', varieties: ['Cumin Seeds (Jeera)', 'Ground Cumin', 'Roasted Jeera'] },
      { name: 'Dhania (Coriander)', varieties: ['Coriander Powder (Dhania)', 'Coriander Seeds', 'Fresh Cilantro'] },
      { name: 'Adrak (Ginger)', varieties: ['Fresh Ginger (Adrak)', 'Ginger Paste', 'Ground Ginger'] },
      { name: 'Lehsun (Garlic)', varieties: ['Garlic Cloves (Lehsun)', 'Minced Garlic', 'Garlic Powder'] },
      { name: 'Hing (Asafoetida)', varieties: ['Compounded Hing', 'Asafoetida Powder'] }
    ]
  },
  {
    id: 'vegetables',
    name: 'Fresh Vegetables & Produce',
    tags: [
      { name: 'Aloo (Potato)', varieties: ['Russet Potato (Aloo)', 'Baby Potatoes', 'Sweet Potato'] },
      { name: 'Pyaz (Onion)', varieties: ['Red Onion (Pyaaz)', 'Yellow Onion', 'White Onion', 'Shallots'] },
      { name: 'Tamatar (Tomato)', varieties: ['Roma Tomatoes (Tamatar)', 'Cherry Tomatoes', 'Tomato Puree'] },
      { name: 'Palak (Spinach)', varieties: ['Fresh Spinach (Palak)', 'Baby Spinach', 'Frozen Spinach'] },
      { name: 'Bhindi & Gobi', varieties: ['Fresh Bhindi (Okra)', 'Cauliflower (Gobi)', 'Green Peas (Matar)'] }
    ]
  },
  {
    id: 'pulses_grains',
    name: 'Dals, Pulses & Grains',
    tags: [
      { name: 'Dal (Lentils)', varieties: ['Toor Dal', 'Moong Dal', 'Masoor Dal (Red)', 'Urad Dal'] },
      { name: 'Chana (Chickpeas)', varieties: ['Kabuli Chana', 'Kala Chana', 'Chickpeas', 'Garbanzo'] },
      { name: 'Rajma (Kidney Beans)', varieties: ['Red Kidney Beans', 'Chitra Rajma'] },
      { name: 'Atta & Rice', varieties: ['Whole Wheat Flour (Atta)', 'All-Purpose Flour (Maida)', 'Basmati Rice', 'Poha'] }
    ]
  }
];

export const POPULAR_INGREDIENT_TAGS = [
  'Paneer', 'Haldi', 'Jeera', 'Aloo', 'Dhania', 'Adrak', 'Lehsun', 'Dal', 'Chana', 'Rajma', 'Bread', 'Chicken', 'Rice', 'Tomato'
];
