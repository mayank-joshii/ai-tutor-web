"""
Sample Data Population Script for AI Tutor
Run with: python manage.py shell < populate_sample_data.py

This script creates:
- Class levels (Class 6-12, JEE, NEET)
- Subjects for each class
- Topics with difficulty levels
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aitutor.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from tutor.models import ClassLevel, Subject, Topic

def populate_data():
    print("🚀 Starting data population...")
    
    # ==================== CLASS LEVELS ====================
    classes_data = [
        ("Class 6", "NCERT Class 6 - Foundation Level"),
        ("Class 7", "NCERT Class 7 - Intermediate"),
        ("Class 8", "NCERT Class 8 - Intermediate"),
        ("Class 9", "NCERT Class 9 - Secondary Education"),
        ("Class 10", "NCERT Class 10 - Secondary Education"),
        ("Class 11", "NCERT Class 11 - Senior Secondary"),
        ("Class 12", "NCERT Class 12 - Senior Secondary"),
        ("JEE Main", "Engineering Entrance Examination - Main"),
        ("NEET", "Medical Entrance Examination"),
    ]
    
    print("\n📚 Creating Class Levels...")
    for class_name, description in classes_data:
        obj, created = ClassLevel.objects.get_or_create(
            class_name=class_name,
            defaults={'description': description}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {class_name}")
    
    # ==================== SUBJECTS FOR CLASS 10 ====================
    print("\n📖 Adding Subjects for Class 10...")
    class_10, _ = ClassLevel.objects.get(class_name="Class 10"), None
    
    class_10_subjects = [
        ("Mathematics", "Algebra, Geometry, Trigonometry, Statistics"),
        ("Science", "Physics, Chemistry, Biology"),
        ("English", "Literature, Grammar, Writing Skills"),
        ("Hindi", "साहित्य और व्याकरण"),
        ("Social Studies", "History, Geography, Political Science, Economics"),
    ]
    
    for subject_name, description in class_10_subjects:
        obj, created = Subject.objects.get_or_create(
            class_level=class_10,
            name=subject_name,
            defaults={'description': description}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {subject_name}")
    
    # ==================== SUBJECTS FOR CLASS 6 ====================
    print("\n📖 Adding Subjects for Class 6...")
    class_6, _ = ClassLevel.objects.get(class_name="Class 6"), None
    
    class_6_subjects = [
        ("Mathematics", "Numbers, Arithmetic, Basic Geometry"),
        ("Science", "Living World, Matter, Energy"),
        ("English", "Literature, Grammar, Communication"),
        ("Hindi", "भाषा और साहित्य"),
        ("Social Studies", "Geography, History, Civics"),
    ]
    
    for subject_name, description in class_6_subjects:
        obj, created = Subject.objects.get_or_create(
            class_level=class_6,
            name=subject_name,
            defaults={'description': description}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {subject_name}")
    
    # ==================== SUBJECTS FOR CLASS 7 ====================
    print("\n📖 Adding Subjects for Class 7...")
    class_7, _ = ClassLevel.objects.get(class_name="Class 7"), None
    
    class_7_subjects = [
        ("Mathematics", "Integers, Fractions, Algebra Basics"),
        ("Science", "Physics, Chemistry, Biology Basics"),
        ("English", "Stories, Poems, Grammar"),
        ("Hindi", "साहित्य और व्याकरण"),
        ("Social Studies", "Geography, History, Civics"),
    ]
    
    for subject_name, description in class_7_subjects:
        obj, created = Subject.objects.get_or_create(
            class_level=class_7,
            name=subject_name,
            defaults={'description': description}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {subject_name}")
    
    # ==================== SUBJECTS FOR CLASS 8 ====================
    print("\n📖 Adding Subjects for Class 8...")
    class_8, _ = ClassLevel.objects.get(class_name="Class 8"), None
    
    class_8_subjects = [
        ("Mathematics", "Rational Numbers, Linear Equations, Geometry"),
        ("Science", "Motion, Forces, Energy, Atoms"),
        ("English", "Literature, Writing, Communication"),
        ("Hindi", "साहित्य, व्याकरण, लेखन"),
        ("Social Studies", "History, Geography, Civics"),
    ]
    
    for subject_name, description in class_8_subjects:
        obj, created = Subject.objects.get_or_create(
            class_level=class_8,
            name=subject_name,
            defaults={'description': description}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {subject_name}")
    
    # ==================== TOPICS FOR CLASS 10 MATHEMATICS ====================
    print("\n🔢 Adding Topics for Class 10 Mathematics...")
    math_subject = Subject.objects.get(class_level=class_10, name="Mathematics")
    
    math_topics = [
        ("Real Numbers", "Classification of numbers, operations, properties", "beginner"),
        ("Polynomials", "Algebraic expressions, polynomial equations, division", "beginner"),
        ("Pair of Linear Equations", "Systems of equations, graphical and algebraic solutions", "beginner"),
        ("Quadratic Equations", "Solving by factoring, completing square, quadratic formula", "intermediate"),
        ("Arithmetic Progressions", "Sequences, series, sum formulas, nth term", "intermediate"),
        ("Triangles", "Properties, similarity, congruence, area", "intermediate"),
        ("Coordinate Geometry", "Distance formula, section formula, straight lines", "intermediate"),
        ("Trigonometry", "Trigonometric ratios, identities, applications", "intermediate"),
        ("Circles", "Circle geometry, tangents, secants, arcs", "advanced"),
        ("Probability", "Experimental and theoretical probability, events", "beginner"),
        ("Statistics", "Mean, median, mode, variance, standard deviation", "beginner"),
    ]
    
    for topic_name, description, level in math_topics:
        obj, created = Topic.objects.get_or_create(
            subject=math_subject,
            name=topic_name,
            defaults={'description': description, 'difficulty_level': level}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {topic_name} ({level})")
    
    # ==================== TOPICS FOR CLASS 10 SCIENCE ====================
    print("\n🔬 Adding Topics for Class 10 Science...")
    science_subject = Subject.objects.get(class_level=class_10, name="Science")
    
    science_topics = [
        ("Chemical Reactions", "Types of reactions, equations, balancing", "beginner"),
        ("Acids and Bases", "pH scale, properties, neutralization", "beginner"),
        ("Metals and Non-metals", "Properties, reactivity, compounds", "beginner"),
        ("Carbon and Compounds", "Organic chemistry, hydrocarbons, bonding", "intermediate"),
        ("Motion", "Distance, displacement, velocity, acceleration", "beginner"),
        ("Force and Laws of Motion", "Newton's laws, friction, momentum", "intermediate"),
        ("Work, Energy, Power", "Kinetic and potential energy, conservation", "intermediate"),
        ("Gravitation", "Newton's law of gravitation, mass vs weight", "intermediate"),
        ("Electricity", "Current, voltage, resistance, circuits", "intermediate"),
        ("Magnetism", "Magnetic fields, electromagnets, Earth's magnetism", "intermediate"),
        ("Light", "Reflection, refraction, lens, human eye", "intermediate"),
        ("Photosynthesis", "Process, products, factors affecting rate", "beginner"),
        ("Nutrition in Animals", "Digestive system, nutrition types", "beginner"),
        ("Respiration", "Aerobic and anaerobic respiration", "beginner"),
        ("Transportation", "Circulatory system, blood, heart", "beginner"),
        ("Excretion", "Urinary system, kidney function", "beginner"),
        ("Reproduction", "Sexual and asexual reproduction, human reproduction", "intermediate"),
        ("Heredity and Evolution", "Genetics, DNA, natural selection", "advanced"),
        ("Control and Coordination", "Nervous system, hormones, reflex arc", "intermediate"),
    ]
    
    for topic_name, description, level in science_topics:
        obj, created = Topic.objects.get_or_create(
            subject=science_subject,
            name=topic_name,
            defaults={'description': description, 'difficulty_level': level}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {topic_name} ({level})")
    
    # ==================== TOPICS FOR CLASS 10 ENGLISH ====================
    print("\n📚 Adding Topics for Class 10 English...")
    english_subject = Subject.objects.get(class_level=class_10, name="English")
    
    english_topics = [
        ("Reading Comprehension", "Understanding texts, answering questions", "beginner"),
        ("Writing Skills", "Essays, letters, reports, creative writing", "beginner"),
        ("Vocabulary", "Synonyms, antonyms, word usage", "beginner"),
        ("Grammar", "Parts of speech, tenses, sentence structure", "beginner"),
        ("Prose", "Understanding stories, character analysis, themes", "intermediate"),
        ("Poetry", "Rhyme scheme, metaphor, symbolism, interpretation", "intermediate"),
        ("Literature", "Novel study, dramatic elements, literary devices", "intermediate"),
        ("Speaking Skills", "Presentation, dialogue, communication", "intermediate"),
        ("Listening", "Note-taking, understanding main ideas", "beginner"),
    ]
    
    for topic_name, description, level in english_topics:
        obj, created = Topic.objects.get_or_create(
            subject=english_subject,
            name=topic_name,
            defaults={'description': description, 'difficulty_level': level}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {topic_name} ({level})")
    
    # ==================== SUBJECTS FOR CLASS 12 ====================
    print("\n📖 Adding Subjects for Class 12...")
    class_12, _ = ClassLevel.objects.get(class_name="Class 12"), None
    
    class_12_subjects = [
        ("Mathematics", "Calculus, Algebra, Matrices, Vectors"),
        ("Physics", "Mechanics, Thermodynamics, Electromagnetism, Optics"),
        ("Chemistry", "Organic, Inorganic, Physical Chemistry"),
        ("Biology", "Botany, Zoology, Genetics"),
        ("English", "Literature, Writing, Communication"),
    ]
    
    for subject_name, description in class_12_subjects:
        obj, created = Subject.objects.get_or_create(
            class_level=class_12,
            name=subject_name,
            defaults={'description': description}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {subject_name}")
    
    # ==================== TOPICS FOR CLASS 12 MATHEMATICS ====================
    print("\n🔢 Adding Topics for Class 12 Mathematics...")
    class_12_math = Subject.objects.get(class_level=class_12, name="Mathematics")
    
    class_12_math_topics = [
        ("Relations and Functions", "Domain, range, function types", "beginner"),
        ("Inverse Trigonometric Functions", "Properties, identities, equations", "intermediate"),
        ("Matrices", "Operations, determinants, inverses", "intermediate"),
        ("Determinants", "Expansion, properties, applications", "intermediate"),
        ("Continuity and Differentiability", "Limits, derivatives, chain rule", "intermediate"),
        ("Applications of Derivatives", "Maxima, minima, optimization", "intermediate"),
        ("Integrals", "Definite and indefinite integrals, substitution", "advanced"),
        ("Applications of Integration", "Area under curves, volumes", "advanced"),
        ("Differential Equations", "Order, degree, solving methods", "advanced"),
        ("Vectors", "Operations, dot product, cross product", "intermediate"),
        ("Three Dimensional Geometry", "Lines, planes, distance formulas", "advanced"),
        ("Linear Programming", "Constraints, optimization problems", "advanced"),
        ("Probability", "Conditional probability, Bayes theorem", "intermediate"),
    ]
    
    for topic_name, description, level in class_12_math_topics:
        obj, created = Topic.objects.get_or_create(
            subject=class_12_math,
            name=topic_name,
            defaults={'description': description, 'difficulty_level': level}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {topic_name} ({level})")
    
    # ==================== TOPICS FOR JEE MAIN ====================
    print("\n🎯 Adding Topics for JEE Main...")
    jee_class, _ = ClassLevel.objects.get(class_name="JEE Main"), None
    
    jee_subjects = [
        ("Physics", "Mechanics, Thermodynamics, Electricity, Magnetism, Optics"),
        ("Chemistry", "Organic, Inorganic, Physical Chemistry"),
        ("Mathematics", "Calculus, Algebra, Coordinate Geometry, Vectors"),
    ]
    
    for subject_name, description in jee_subjects:
        obj, created = Subject.objects.get_or_create(
            class_level=jee_class,
            name=subject_name,
            defaults={'description': description}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {subject_name}")
    
    # ==================== TOPICS FOR NEET ====================
    print("\n⚕️ Adding Topics for NEET...")
    neet_class, _ = ClassLevel.objects.get(class_name="NEET"), None
    
    neet_subjects = [
        ("Biology", "Cell Biology, Genetics, Evolution, Ecology, Botany, Zoology"),
        ("Physics", "Mechanics, Thermodynamics, Optics, Modern Physics"),
        ("Chemistry", "Organic, Inorganic, Physical Chemistry"),
    ]
    
    for subject_name, description in neet_subjects:
        obj, created = Subject.objects.get_or_create(
            class_level=neet_class,
            name=subject_name,
            defaults={'description': description}
        )
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"  {status}: {subject_name}")
    
    print("\n" + "="*50)
    print("✅ Data Population Complete!")
    print("="*50)
    
    # Print statistics
    print(f"\n📊 Summary:")
    print(f"  Classes: {ClassLevel.objects.count()}")
    print(f"  Subjects: {Subject.objects.count()}")
    print(f"  Topics: {Topic.objects.count()}")
    print("\n✨ Your AI Tutor is ready to use!")

if __name__ == "__main__":
    populate_data()
