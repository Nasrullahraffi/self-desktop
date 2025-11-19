"""
Education App Models
Handles skills, education history, and certifications
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator


class Skill(models.Model):
    """Technical and soft skills with proficiency levels"""

    SKILL_CATEGORIES = [
        ('frontend', 'Frontend Development'),
        ('backend', 'Backend Development'),
        ('database', 'Database'),
        ('devops', 'DevOps & Tools'),
        ('design', 'Design'),
        ('soft', 'Soft Skills'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, help_text="Skill name")
    category = models.CharField(
        max_length=20,
        choices=SKILL_CATEGORIES,
        default='other'
    )
    proficiency = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency percentage (0-100)"
    )
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="FontAwesome or Devicon class (e.g., fab fa-python)"
    )
    color = models.CharField(
        max_length=20,
        default='success',
        help_text="Bootstrap color class (primary, success, info, warning, danger)"
    )
    description = models.TextField(
        blank=True,
        help_text="Brief description of your experience with this skill"
    )

    # Display Settings
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower = first)"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['order', 'category', '-proficiency']

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"

    def get_proficiency_label(self):
        """Return proficiency level as label"""
        if self.proficiency >= 90:
            return "Expert"
        elif self.proficiency >= 70:
            return "Advanced"
        elif self.proficiency >= 50:
            return "Intermediate"
        else:
            return "Beginner"


class Education(models.Model):
    """Educational background"""

    DEGREE_TYPES = [
        ('phd', 'Ph.D.'),
        ('masters', 'Master\'s Degree'),
        ('bachelors', 'Bachelor\'s Degree'),
        ('associate', 'Associate Degree'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
        ('bootcamp', 'Bootcamp'),
        ('other', 'Other'),
    ]

    institution = models.CharField(max_length=200, help_text="School/University name")
    degree = models.CharField(
        max_length=20,
        choices=DEGREE_TYPES,
        help_text="Degree type"
    )
    field_of_study = models.CharField(
        max_length=200,
        help_text="Major/Field of study"
    )
    description = models.TextField(
        blank=True,
        help_text="Description, achievements, relevant coursework"
    )

    # Dates
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if current")
    is_current = models.BooleanField(default=False, help_text="Currently studying")

    # Additional Info
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Grade Point Average"
    )
    location = models.CharField(max_length=200, blank=True, help_text="City, Country")
    logo = models.ImageField(
        upload_to='education/',
        blank=True,
        null=True,
        help_text="Institution logo"
    )

    # Display Settings
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.get_degree_display()} in {self.field_of_study} - {self.institution}"


class Certification(models.Model):
    """Professional certifications and courses"""

    name = models.CharField(max_length=200, help_text="Certification name")
    issuing_organization = models.CharField(
        max_length=200,
        help_text="Issuing organization"
    )
    credential_id = models.CharField(
        max_length=200,
        blank=True,
        help_text="Credential ID/License number"
    )
    credential_url = models.URLField(
        blank=True,
        validators=[URLValidator()],
        help_text="Verification URL"
    )
    issue_date = models.DateField()
    expiry_date = models.DateField(
        blank=True,
        null=True,
        help_text="Leave blank if no expiration"
    )
    description = models.TextField(
        blank=True,
        help_text="Description and skills gained"
    )
    logo = models.ImageField(
        upload_to='certifications/',
        blank=True,
        null=True,
        help_text="Certification badge/logo"
    )

    # Display Settings
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['order', '-issue_date']

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"

    @property
    def is_expired(self):
        """Check if certification is expired"""
        if self.expiry_date:
            from datetime import date
            return date.today() > self.expiry_date
        return False

