### Test SYSTEM
src/
├── assets/          # Global styles, fonts, base images
├── components/      # Truly global, domain-agnostic UI elements (BaseButton, BaseModal)
├── composables/     # App-wide global Composition API hooks (useAuth, useTheme)
├── router/          # App navigation mapping
├── features/        #  Organized by domain/business capability
│   ├── auth/
│   │   ├── components/    # Feature-specific components (LoginForm, RegisterCard)
│   │   ├── composables/   # Feature-specific logic (useLoginValidation)
│   │   ├── store.ts       # Pinia store isolated to Auth
│   │   └── types.ts       # TypeScript models for Auth
│   └── products/
│       ├── components/    # ProductCard, ProductGrid
│       └── store.ts       
├── views/           # Page containers mapped directly to routes (HomeView, DashboardView)
├── App.vue          # Root Vue component
└── main.ts          # Application entry point
