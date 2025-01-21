// Protein analysis module

mod protein_calculator;

pub use protein_calculator::{
    analyze_particle_distribution,
    calculate_protein_recovery,
    calculate_separation_efficiency,
};
